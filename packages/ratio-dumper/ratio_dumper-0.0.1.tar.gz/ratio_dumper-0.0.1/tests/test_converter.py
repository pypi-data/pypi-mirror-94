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

from ratio_dumper import SerialDriver, convert_to_xml
from tests.utilities import MockSerialIO


def test_sample_dive():
    sd = SerialDriver(None)
    with (Path(__file__).parent / 'data' / 'dive_1.json').open('r') as fh:
        sd._serial = MockSerialIO(json.loads(fh.read()))

    dive = sd.get_dive(1)

    generated_xml = convert_to_xml(dive)
    with (Path(__file__).parent / 'data' / 'sample.xml').open('r') as fh:
        expected_xml = fh.read().strip()

    assert generated_xml == expected_xml
