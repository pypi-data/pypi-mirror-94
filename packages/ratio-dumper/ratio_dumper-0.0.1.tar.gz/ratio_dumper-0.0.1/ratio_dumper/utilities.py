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
import logging
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.cElementTree import Element, SubElement

from crcmod.predefined import mkCrcFun

from .models import Dive

logger: logging.Logger = logging.getLogger(__name__)


class CrcHelper:
    @staticmethod
    def calculate(payload: bytes) -> int:
        '''Calculate the CRC for a payload in bytes.'''
        return mkCrcFun('crc-ccitt-false')(payload)

    @staticmethod
    def encode(crc: int) -> str:
        '''Bit encode a calculated CRC in 2 bytes.'''
        return f'{(crc >> 8) & 255:02x}{crc & 255:02x}'

    @staticmethod
    def decode(crc_byte1: int, crc_byte2: int) -> int:
        '''Bit decode a calculated CRC in 2 bytes.'''
        return (crc_byte1 << 8) | (crc_byte2 << 0)


class ByteConverter:
    @staticmethod
    def to_int8(data: bytes) -> int:
        """Convert 1 byte into an un-signed 8bit integer."""
        if len(data) != 1:
            raise ValueError(f"to_int8 requires one bytes ({data})")
        return data[0]

    @staticmethod
    def to_uint8(data: bytes) -> int:
        """Convert 1 byte into a signed 8bit integer."""
        if len(data) != 1:
            raise ValueError(f"to_uint8 requires one bytes ({data})")
        return data[0] & 255

    @staticmethod
    def to_int16(data: bytes) -> int:
        """Convert 2 bytes into a signed 16bit integer."""
        if len(data) != 2:
            raise ValueError(f"to_int16 requires two bytes ({data})")
        return (data[1] << 8) | (data[0] & 255)

    @staticmethod
    def to_uint16(data: bytes) -> int:
        """Convert 2 bytes into an un-signed 16bit integer."""
        if len(data) != 2:
            raise ValueError(f"to_uint16 requires two bytes ({data})")
        return ((data[1] & 255) << 8) | (data[0] & 255)

    @staticmethod
    def to_int32(data: bytes) -> int:
        """Convert 4 bytes into a signed 32bit integer."""
        if len(data) != 4:
            raise ValueError(f"to_int32 requires four bytes ({data})")
        return (data[3] << 24 |
                (data[2] & 255) << 16 |
                (data[1] & 255) << 8 |
                (data[0] & 255))

    @staticmethod
    def to_uint32(data: bytes) -> int:
        """Convert 4 bytes into an un-signed 32bit integer."""
        if len(data) != 4:
            raise ValueError(f"to_uint32 requires four bytes ({data})")
        return ((data[3] & 255) << 24 |
                (data[2] & 255) << 16 |
                (data[1] & 255) << 8 |
                (data[0] & 255))


def convert_to_xml(dive: Dive) -> str:
    diveSegment = Element("diveSegment", version="1.1")

    segmentHeader = SubElement(diveSegment, "segmentHeader")
    SubElement(segmentHeader, 'equipmentType').text = '100'
    SubElement(segmentHeader, 'activeUser').text = str(dive.active_user)
    SubElement(segmentHeader, 'diveSamples').text = str(dive.dive_sample_count)
    SubElement(segmentHeader, 'monotonicTimeS').text = str(dive.monotonic_time)
    SubElement(segmentHeader, 'UTCStartingTimeS').text = str(dive.utc_starting_time)
    SubElement(segmentHeader, 'surfacePressureMbar').text = str(dive.surface_pressure)
    SubElement(segmentHeader, 'lastSurfaceTimeS').text = str(
        dive.last_surface_time
        if dive.last_surface_time < dive.utc_starting_time else
        -1
    )
    SubElement(segmentHeader, 'desaturationTimeS').text = str(dive.desaturation_time)
    SubElement(segmentHeader, 'depthMax').text = str(int(dive.depth_max * 100))
    SubElement(segmentHeader, 'decostopDepth1Dm').text = str(
        int(dive.decompression_settings.decostop_depth_1 * 100)
    )
    SubElement(segmentHeader, 'decostopDepth2Dm').text = str(
        int(dive.decompression_settings.decostop_depth_2 * 100)
    )
    SubElement(segmentHeader, 'decostopStep1Dm').text = str(
        dive.decompression_settings.decostop_step_1
    )
    SubElement(segmentHeader, 'decostopStep2Dm').text = str(
        dive.decompression_settings.decostop_step_2
    )
    SubElement(segmentHeader, 'decostopStep3Dm').text = str(
        dive.decompression_settings.decostop_step_3
    )
    SubElement(segmentHeader, 'deepStopAlg').text = str(dive.deep_stop_algorithm)
    SubElement(segmentHeader, 'safetyStopDepthDm').text = str(int(dive.safety_stop_depth * 100))
    SubElement(segmentHeader, 'safetyStopMin').text = str(dive.safety_stop_time)
    SubElement(segmentHeader, 'diveMode').text = str(dive.dive_mode.value)
    SubElement(segmentHeader, 'water').text = str(dive.water.value)
    SubElement(segmentHeader, 'alarmsGeneral').text = str(dive.alarms_general)
    SubElement(segmentHeader, 'alarmTime').text = str(dive.alarm_time)
    SubElement(segmentHeader, 'alarmDepth').text = str(int(dive.alarm_depth * 100))
    SubElement(segmentHeader, 'backlightLevel').text = str(dive.backlight_level)
    SubElement(segmentHeader, 'backlightMode').text = str(dive.backlight_mode)
    SubElement(segmentHeader, 'softwareVersion').text = str(dive.software_version.as_numeric)
    SubElement(segmentHeader, 'alertFlag').text = str(dive.alert_flag)
    SubElement(segmentHeader, 'freeUserSettings').text = str(dive.free_user_settings)
    SubElement(segmentHeader, 'timezoneIdx').text = str(dive.timezone_id)
    SubElement(segmentHeader, 'avgDepth').text = str(int(dive.avg_depth * 100))
    SubElement(segmentHeader, 'dum6').text = str(dive.dum_6)
    SubElement(segmentHeader, 'dum7').text = str(dive.dum_7)
    SubElement(segmentHeader, 'dum8').text = str(dive.dum_8)

    samples = SubElement(diveSegment, "samples")

    for sample in dive.samples:
        diveSample = SubElement(samples, "sample")
        SubElement(diveSample, 'vbatCV').text = str(int(sample.battery_voltage * 100))
        SubElement(diveSample, 'runtimeS').text = str(sample.runtime_seconds)
        SubElement(diveSample, 'depthDm').text = str(int(sample.depth * 10))
        SubElement(diveSample, 'temperatureDc').text = str(int(sample.temperature * 10))
        SubElement(diveSample, 'activeMixO2Percent').text = str(
            sample.active_mix.o2_percentage
        )
        SubElement(diveSample, 'activeMixHePercent').text = str(
            sample.active_mix.he_percentage
        )
        SubElement(diveSample, 'suggestedMixO2Percent').text = str(
            sample.suggested_mix.o2_percentage
        )
        SubElement(diveSample, 'suggestedMixHePercent').text = str(
            sample.suggested_mix.he_percentage
        )
        SubElement(diveSample, 'activeAlgorithm').text = str(sample.active_algorithm.value)
        SubElement(diveSample, 'buhlGfHigh').text = str(
            sample.algorithm_settings.buhlmann.gradient_factor_high
        )
        SubElement(diveSample, 'buhlGfLow').text = str(
            sample.algorithm_settings.buhlmann.gradient_factor_low
        )
        SubElement(diveSample, 'vpmR0').text = str(sample.algorithm_settings.vpm.r0)
        SubElement(diveSample, 'modeOCSCRCCRGauge').text = str(sample.mode_oc_scr_ccr_gauge)
        SubElement(diveSample, 'maxPPO2OrSetpoint').text = str(
            int(sample.max_ppo2_or_setpoint * 1000)
        )
        SubElement(diveSample, 'firstStopDepth').text = str(int(sample.first_stop_depth * 10))
        SubElement(diveSample, 'firstStopTime').text = str(sample.first_stop_time)
        SubElement(diveSample, 'NDLOrTTS').text = str(sample.ndl_or_tts)
        SubElement(diveSample, 'OTU').text = str(sample.otu)
        SubElement(diveSample, 'CNS').text = str(sample.cns)
        SubElement(diveSample, 'tissueGroup1Percent').text = str(sample.tissue_group1_percent)
        SubElement(diveSample, 'tissueGroup2Percent').text = str(sample.tissue_group2_percent)
        SubElement(diveSample, 'tissueGroup3Percent').text = str(sample.tissue_group3_percent)
        SubElement(diveSample, 'tissueGroup4Percent').text = str(sample.tissue_group4_percent)
        SubElement(diveSample, 'tissueGroup5Percent').text = str(sample.tissue_group5_percent)
        SubElement(diveSample, 'tissueGroup6Percent').text = str(sample.tissue_group6_percent)
        SubElement(diveSample, 'tissueGroup7Percent').text = str(sample.tissue_group7_percent)
        SubElement(diveSample, 'tissueGroup8Percent').text = str(sample.tissue_group8_percent)
        SubElement(diveSample, 'tissueGroup9Percent').text = str(sample.tissue_group9_percent)
        SubElement(diveSample, 'tissueGroup10Percent').text = str(sample.tissue_group10_percent)
        SubElement(diveSample, 'tissueGroup11Percent').text = str(sample.tissue_group11_percent)
        SubElement(diveSample, 'tissueGroup12Percent').text = str(sample.tissue_group12_percent)
        SubElement(diveSample, 'tissueGroup13Percent').text = str(sample.tissue_group13_percent)
        SubElement(diveSample, 'tissueGroup14Percent').text = str(sample.tissue_group14_percent)
        SubElement(diveSample, 'tissueGroup15Percent').text = str(sample.tissue_group15_percent)
        SubElement(diveSample, 'tissueGroup16Percent').text = str(sample.tissue_group16_percent)
        SubElement(diveSample, 'enabledMixSensors').text = str(sample.enabled_mix_sensors)
        SubElement(diveSample, 'setPointMode').text = str(sample.set_point_mode)
        SubElement(diveSample, 'tankPressure').text = str(sample.tank_pressure)
        SubElement(diveSample, 'compassLog').text = str(sample.compass_log)
        SubElement(diveSample, 'reserved2').text = str(sample.reserved_2)

    # Export out the tree as a string
    xmlString = ElementTree.tostring(diveSegment, encoding='utf-8')

    # Re-format our string to be pretty
    return minidom.parseString(xmlString).toprettyxml(encoding='UTF-8',
                                                      indent='    ').decode().strip()
