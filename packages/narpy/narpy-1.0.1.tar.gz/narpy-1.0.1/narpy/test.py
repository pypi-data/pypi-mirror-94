import unittest
from narpy import *

__copyright__="""
    narpy - A simple NASA AMES file Reader for Python
    Copyright (C) 2021 Jago Strong-Wright

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

example_loc="test.na"
class TestBasics(unittest.TestCase):
    
    def test_comment(self):
        self.maxDiff=None
        example_comment="""Example of FFI 1001 (a).
This example illustrating NASA Ames file format index 1001 is based on the US Standard
Atmosphere 1976 as quoted in G. Brasseur and S. Solomon, Aeronomy of the Middle
Atmosphere, Reidel, 1984 (p. 46). It provides typical values of middle latitude averaged air
concentration and temperature as a function of height (expressed here as the pressure
level). The first date on line 7 (1st of January 1976) is fictitious since the parameters are
yearly averages. We have inserted 3 additional lines into the original table near the tropo-go
pause and stratopause levels, to illustrate the use of the "missing value" flags (see line 12).
12
The files included in this data set illustrate each of the 9 NASA Ames file format indices
(FFI). A detailed description of the NASA Ames format can be found on the Web site of the
British Atmospheric Data Centre at http://www.badc.rl.ac.uk/help/formats/NASA-Ames/
E-mail contact: badc@rl.ac.uk
Reference: S. E. Gaines and R. S. Hipskind, Format Specification for Data Exchange,
Version 1.3, 1998. This work can be found at
http://cloud1.arc.nasa.gov/solve/archiv/archive.tutorial.html and a copy of it at
http://www.badc.rl.ac.uk/help/formats/NASA-Ames/G-and-H-June-1998.html

    Pressure    Concentration   Temperature
      (mb)         (cm-3)           (K)
"""
        self.assertEqual(file(example_loc).comment,example_comment)


    def test_length(self):
        self.assertEqual(len(file(example_loc)["Pressure (hPa)"].data),28)

    def test_variable(self):
        self.assertEqual(file(example_loc)["Temperature (degrees K)"].data[3],217)

if __name__=="__main__":
    unittest.main()