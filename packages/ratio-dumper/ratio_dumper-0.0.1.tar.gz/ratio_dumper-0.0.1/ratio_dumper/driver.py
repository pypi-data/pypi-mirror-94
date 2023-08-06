'''
ratio_dumper - Ratio iX5M Log Dumper

MIT License

Copyright (c) 2021 Damian Zaremba

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from __future__ import annotations

import logging
from io import BytesIO
from types import TracebackType
from typing import Tuple, Set, List, Optional, Type

from serial import Serial

from .models import (Dive,
                     DiveSample,
                     DiveMode,
                     WaterType,
                     SoftwareVersion,
                     DecompressionAlgorithm,
                     DecompressionAlgorithmSettings,
                     GasMix,
                     DiveDecompressionSettings,
                     DecompressionAlgorithmBuhlmannSettings,
                     DecompressionAlgorithmVpmSettings)
from .utilities import ByteConverter, CrcHelper

logger: logging.Logger = logging.getLogger(__name__)


class SerialDriver:
    _serial: Serial

    def __init__(self, serial_path: Optional[str]) -> None:
        # pyre-ignore[16]
        self._serial = Serial(port=serial_path, baudrate=115200, timeout=1)

    def __enter__(self) -> SerialDriver:
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self._serial.close()

    def _encode_payload(self, command: int, options: List[int]) -> bytes:
        '''Encode a set of commands with a CRC.'''
        # Packet layout:
        #  85 = byte, START marker
        #  <variable> = byte, command
        #  <..> = byte, variable length options
        #  <variable> = 2 bytes, CRC of the payload
        payload = f'{85:02x}{len(options) + 1:02x}{command:02x}'
        for option in options:
            payload += f'{option:02x}'
        payload += CrcHelper.encode(CrcHelper.calculate(bytes.fromhex(payload)))

        logger.debug(f'Encoded payload: {payload}')
        return bytes.fromhex(payload)

    def _decode_payload(self, command: int) -> Tuple[BytesIO, Optional[int]]:
        '''Decode a response payload.'''
        # Response layout:
        #  85 = byte, START marker
        #  <variable> = byte, command
        #  <variable> = byte, length of payload
        #  <..> = byte, variable length payload
        #  <variable> = byte, ACK or NAK marker
        #  <variable> = 2 bytes, CRC of the payload
        packet_header = self._serial.read(1)
        if not packet_header:
            return BytesIO(), -1

        assert packet_header[0] == 85

        packet_length = self._serial.read(1)
        read_size = int(packet_length.hex(), 16)
        assert read_size > 2 and read_size < 255

        packet_body = self._serial.read(read_size + 2)
        assert len(packet_body) == read_size + 2
        logger.debug(f'Decoded payload: {(packet_header + packet_length + packet_body).hex()}')

        payload, crc = packet_body[:read_size], packet_body[read_size:]
        expected_crc = CrcHelper.calculate(packet_header + packet_length + payload)

        assert expected_crc == CrcHelper.decode(crc[0], crc[1])
        assert payload[0] == command

        # ACK indicates a success
        # Return all data without the command and ack byte
        if payload[-1] == 6:
            return BytesIO(payload[1:-1]), None

        # NAK indicates an error
        # Return the first byte as the error code
        elif payload[-1] == 21:
            error_code = (payload[1] & 255)
            logger.warning(f'Hit NAK marker: {error_code}')
            return BytesIO(), error_code

        # Unknown response
        else:
            logger.critical(f'Unknown response: {payload}')
            return BytesIO(), -1

    def get_dive_ids(self) -> Optional[Set[int]]:
        '''Query a device for all dives.'''
        self._serial.write(self._encode_payload(120, [141]))
        payload, error_code = self._decode_payload(120)
        if error_code is not None:
            logger.critical(f'get_dive_ids got {error_code}')
            return None

        first_dive = ByteConverter.to_uint16(payload.read(2))
        last_dive = ByteConverter.to_uint16(payload.read(2))
        return set(range(first_dive, last_dive + 1))

    def _get_dive_sample(self, sample_id: int) -> Optional[DiveSample]:
        """Query a device for a specific dive sample."""
        self._serial.write(self._encode_payload(122, [sample_id & 255, (sample_id >> 8) & 255]))
        payload, error_code = self._decode_payload(122)
        if error_code is not None:
            logger.critical(f'get_dive_sample got {error_code}')
            return None

        sample = DiveSample(
            battery_voltage=(ByteConverter.to_uint16(payload.read(2)) / 100.0),
            runtime_seconds=ByteConverter.to_uint32(payload.read(4)),
            depth=ByteConverter.to_uint16(payload.read(2)) / 10.0,
            temperature=ByteConverter.to_uint16(payload.read(2)) / 10.0,
            active_mix=GasMix(
                ByteConverter.to_uint8(payload.read(1)),
                ByteConverter.to_uint8(payload.read(1)),
            ),
            suggested_mix=GasMix(
                ByteConverter.to_uint8(payload.read(1)),
                ByteConverter.to_uint8(payload.read(1)),
            ),
            active_algorithm=DecompressionAlgorithm(ByteConverter.to_uint8(payload.read(1))),
            algorithm_settings=DecompressionAlgorithmSettings(
                buhlmann=DecompressionAlgorithmBuhlmannSettings(
                    gradient_factor_high=ByteConverter.to_uint8(payload.read(1)),
                    gradient_factor_low=ByteConverter.to_uint8(payload.read(1)),
                ),
                vpm=DecompressionAlgorithmVpmSettings(
                    r0=ByteConverter.to_uint8(payload.read(1)),
                ),
            ),
            mode_oc_scr_ccr_gauge=ByteConverter.to_uint8(payload.read(1)),
            max_ppo2_or_setpoint=(ByteConverter.to_uint16(payload.read(2)) / 1000.0),
            first_stop_depth=ByteConverter.to_uint16(payload.read(2)) / 10.0,
            first_stop_time=ByteConverter.to_uint16(payload.read(2)),
            ndl_or_tts=ByteConverter.to_uint16(payload.read(2)),
            otu=ByteConverter.to_uint16(payload.read(2)),
            cns=ByteConverter.to_uint16(payload.read(2)),
            tissue_group1_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group2_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group3_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group4_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group5_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group6_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group7_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group8_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group9_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group10_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group11_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group12_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group13_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group14_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group15_percent=ByteConverter.to_uint8(payload.read(1)),
            tissue_group16_percent=ByteConverter.to_uint8(payload.read(1)),
            enabled_mix_sensors=ByteConverter.to_uint8(payload.read(1)),
            set_point_mode=ByteConverter.to_uint8(payload.read(1)),
            tank_pressure=ByteConverter.to_uint8(payload.read(1)),
            compass_log=ByteConverter.to_int16(payload.read(2)),
            reserved_2=ByteConverter.to_int16(payload.read(2)),
        )
        logger.debug(f"Decoded dive sample: {sample}")
        return sample

    def get_dive(self, dive_id: int) -> Optional[Dive]:
        '''Query a device for a specific dive.'''
        self._serial.write(self._encode_payload(121, [dive_id & 255, (dive_id >> 8) & 255]))
        payload, error_code = self._decode_payload(121)
        if error_code is not None:
            logger.critical(f'get_dive got {error_code}')
            return None

        # Decode the segmentHeader
        dive = Dive(
            active_user=ByteConverter.to_uint8(payload.read(1)),
            dive_sample_count=ByteConverter.to_uint16(payload.read(2)),
            monotonic_time=ByteConverter.to_uint32(payload.read(4)),
            utc_starting_time=ByteConverter.to_uint32(payload.read(4)),
            surface_pressure=ByteConverter.to_uint16(payload.read(2)),
            last_surface_time=ByteConverter.to_int32(payload.read(4)),
            desaturation_time=ByteConverter.to_int32(payload.read(4)),
            depth_max=ByteConverter.to_uint16(payload.read(2)) / 100.0,
            decompression_settings=DiveDecompressionSettings(
                decostop_depth_1=ByteConverter.to_uint16(payload.read(2)) / 100.0,
                decostop_depth_2=ByteConverter.to_uint16(payload.read(2)) / 100.0,
                decostop_step_1=ByteConverter.to_uint8(payload.read(1)),
                decostop_step_2=ByteConverter.to_uint8(payload.read(1)),
                decostop_step_3=ByteConverter.to_uint8(payload.read(1)),
            ),
            deep_stop_algorithm=ByteConverter.to_uint8(payload.read(1)),
            safety_stop_depth=ByteConverter.to_uint8(payload.read(1)) / 100.0,
            safety_stop_time=ByteConverter.to_uint8(payload.read(1)),
            dive_mode=DiveMode(ByteConverter.to_uint8(payload.read(1))),
            water=WaterType(ByteConverter.to_uint8(payload.read(1))),
            alarms_general=ByteConverter.to_uint8(payload.read(1)),
            alarm_time=ByteConverter.to_uint16(payload.read(2)),
            alarm_depth=ByteConverter.to_uint16(payload.read(2)) / 100.0,
            backlight_level=ByteConverter.to_uint8(payload.read(1)),
            backlight_mode=ByteConverter.to_uint8(payload.read(1)),
            software_version=SoftwareVersion(ByteConverter.to_uint32(payload.read(4))),
            alert_flag=ByteConverter.to_uint8(payload.read(1)),
            free_user_settings=ByteConverter.to_uint8(payload.read(1)),
            timezone_id=ByteConverter.to_uint8(payload.read(1)),
            avg_depth=ByteConverter.to_uint16(payload.read(2)) / 100.0,
            dum_6=ByteConverter.to_uint8(payload.read(1)),
            dum_7=ByteConverter.to_uint8(payload.read(1)),
            dum_8=ByteConverter.to_uint8(payload.read(1)),
            samples=[],
        )
        logger.debug(f"Decoded dive header: {dive}")

        # Decode the samples
        for sample_id in range(1, dive.dive_sample_count + 1):
            sample = self._get_dive_sample(sample_id)
            if sample is None:
                return None
            dive.samples.append(sample)

        return dive
