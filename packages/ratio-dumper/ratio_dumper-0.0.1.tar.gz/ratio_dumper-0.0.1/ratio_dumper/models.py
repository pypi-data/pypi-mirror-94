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
from enum import Enum
from typing import List

from dataclasses import dataclass


class DiveMode(Enum):
    OC = 0


class WaterType(Enum):
    Salt = 0
    Fresh = 1


class DecompressionAlgorithm(Enum):
    buhlmann_16b = 2


class SoftwareVersion:
    version: int
    major: str
    minor: str
    patch: str
    build: str

    def __init__(self, version: int) -> None:
        self.version: int = version
        self.major: str = f'{int((version / 10000000) % 100)}'
        self.minor: str = f'{int((version / 100000) % 100)}'
        self.patch: str = f'{int((version / 1000) % 100)}'
        self.build: str = f'{version % 1000:03d}'

    @property
    def as_release(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}/{self.build}'

    @property
    def as_numeric(self) -> int:
        return self.version


@dataclass(frozen=True)
class GasMix:
    o2_percentage: int
    he_percentage: int

    @property
    def mix(self) -> str:
        return f'{self.o2_percentage}/{self.he_percentage}'


@dataclass(frozen=True)
class DecompressionAlgorithmVpmSettings:
    r0: int


@dataclass(frozen=True)
class DecompressionAlgorithmBuhlmannSettings:
    gradient_factor_low: int
    gradient_factor_high: int


@dataclass(frozen=True)
class DecompressionAlgorithmSettings:
    buhlmann: DecompressionAlgorithmBuhlmannSettings
    vpm: DecompressionAlgorithmVpmSettings


@dataclass(frozen=True)
class DiveDecompressionSettings:
    decostop_depth_1: float
    decostop_depth_2: float
    decostop_step_1: int
    decostop_step_2: int
    decostop_step_3: int


@dataclass(frozen=True)
class DiveSample:
    battery_voltage: float
    runtime_seconds: int
    depth: float
    temperature: float
    active_mix: GasMix
    suggested_mix: GasMix
    active_algorithm: DecompressionAlgorithm
    algorithm_settings: DecompressionAlgorithmSettings
    mode_oc_scr_ccr_gauge: int
    max_ppo2_or_setpoint: float
    first_stop_depth: float
    first_stop_time: int
    ndl_or_tts: int
    otu: int
    cns: int
    tissue_group1_percent: int
    tissue_group2_percent: int
    tissue_group3_percent: int
    tissue_group4_percent: int
    tissue_group5_percent: int
    tissue_group6_percent: int
    tissue_group7_percent: int
    tissue_group8_percent: int
    tissue_group9_percent: int
    tissue_group10_percent: int
    tissue_group11_percent: int
    tissue_group12_percent: int
    tissue_group13_percent: int
    tissue_group14_percent: int
    tissue_group15_percent: int
    tissue_group16_percent: int
    enabled_mix_sensors: int
    set_point_mode: int
    tank_pressure: int
    compass_log: int
    reserved_2: int


@dataclass(frozen=True)
class Dive:
    active_user: int
    dive_sample_count: int
    monotonic_time: int
    utc_starting_time: int
    surface_pressure: int
    last_surface_time: int
    desaturation_time: int
    depth_max: float
    decompression_settings: DiveDecompressionSettings
    deep_stop_algorithm: int
    safety_stop_depth: float
    safety_stop_time: int
    dive_mode: DiveMode
    water: WaterType
    alarms_general: int
    alarm_time: int
    alarm_depth: float
    backlight_level: int
    backlight_mode: int
    software_version: SoftwareVersion
    alert_flag: int
    free_user_settings: int
    timezone_id: int
    avg_depth: float
    dum_6: int
    dum_7: int
    dum_8: int
    samples: List[DiveSample]
