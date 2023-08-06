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
import json
from pathlib import Path

from ratio_dumper import SerialDriver
from ratio_dumper.models import DiveMode, WaterType, DecompressionAlgorithm
from tests.utilities import MockSerialIO


def test_get_dive_ids():
    sd = SerialDriver(None)
    sd._serial = MockSerialIO({
        '5502788de20b': '55067801000400064d48',
    })
    assert sd.get_dive_ids() == {1, 2, 3, 4}


def test_get_dive_1():
    sd = SerialDriver(None)
    with (Path(__file__).parent / 'data' / 'dive_1.json').open('r') as fh:
        sd._serial = MockSerialIO(json.loads(fh.read()))

    dive = sd.get_dive(1)

    assert dive.dive_sample_count == 29
    assert dive.avg_depth == 4.65
    assert dive.dive_mode == DiveMode.OC
    assert dive.utc_starting_time == 409911594
    assert dive.last_surface_time == 4294967295
    assert dive.depth_max == 8.91
    assert dive.water == WaterType.Fresh

    assert dive.samples[0].runtime_seconds == 10
    assert dive.samples[0].depth == 1.9
    assert dive.samples[0].temperature == 8.4
    assert dive.samples[0].ndl_or_tts == 32767
    assert dive.samples[0].battery_voltage == 3.82
    assert dive.samples[0].max_ppo2_or_setpoint == 1.4

    assert dive.samples[0].active_mix.o2_percentage == 21
    assert dive.samples[0].active_mix.he_percentage == 0
    assert dive.samples[0].active_mix.mix == '21/0'

    assert dive.samples[0].suggested_mix.o2_percentage == 21
    assert dive.samples[0].suggested_mix.he_percentage == 0
    assert dive.samples[0].suggested_mix.mix == '21/0'

    assert dive.samples[0].active_algorithm == DecompressionAlgorithm.buhlmann_16b
    assert dive.samples[0].algorithm_settings.buhlmann.gradient_factor_high == 80
    assert dive.samples[0].algorithm_settings.buhlmann.gradient_factor_low == 30


def test_get_dive_4():
    sd = SerialDriver(None)
    with (Path(__file__).parent / 'data' / 'dive_4.json').open('r') as fh:
        sd._serial = MockSerialIO(json.loads(fh.read()))

    dive = sd.get_dive(4)

    assert dive.dive_sample_count == 151
    assert dive.avg_depth == 7.19
    assert dive.dive_mode == DiveMode.OC
    assert dive.utc_starting_time == 411414788
    assert dive.last_surface_time == 4294967295
    assert dive.depth_max == 10.97
    assert dive.water == WaterType.Fresh

    assert dive.samples[0].runtime_seconds == 10
    assert dive.samples[0].depth == 2.0
    assert dive.samples[0].temperature == 4.1
    assert dive.samples[0].ndl_or_tts == 32767
    assert dive.samples[0].battery_voltage == 3.62
    assert dive.samples[0].max_ppo2_or_setpoint == 1.4

    assert dive.samples[0].active_mix.o2_percentage == 21
    assert dive.samples[0].active_mix.he_percentage == 0
    assert dive.samples[0].active_mix.mix == '21/0'

    assert dive.samples[0].suggested_mix.o2_percentage == 21
    assert dive.samples[0].suggested_mix.he_percentage == 0
    assert dive.samples[0].suggested_mix.mix == '21/0'

    assert dive.samples[0].active_algorithm == DecompressionAlgorithm.buhlmann_16b
    assert dive.samples[0].algorithm_settings.buhlmann.gradient_factor_high == 80
    assert dive.samples[0].algorithm_settings.buhlmann.gradient_factor_low == 30

    assert dive.samples[75].runtime_seconds == 760
    assert dive.samples[75].depth == 10.3
    assert dive.samples[75].temperature == 4.3
    assert dive.samples[75].ndl_or_tts == 32767
    assert dive.samples[75].battery_voltage == 3.62
    assert dive.samples[75].max_ppo2_or_setpoint == 1.4

    assert dive.samples[-1].runtime_seconds == 1510
    assert dive.samples[-1].depth == 1.2
    assert dive.samples[-1].temperature == 4.3
    assert dive.samples[-1].ndl_or_tts == 32767
    assert dive.samples[-1].battery_voltage == 3.61
    assert dive.samples[-1].max_ppo2_or_setpoint == 1.4
