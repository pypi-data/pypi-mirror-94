"""narpy - NASA AMES (na) Reader Python

A simple NASA AMES file Reader for Python

See http://cedadocs.ceda.ac.uk/73/4/index.html for an explanation of the forma

Example:
    Loading a file and getting a variable names "x"::

        $ python
        >>> import narpy as na
        >>> f=na.file("example.na")
        >>> f["x"].data

Todo:
    * Add interpolation method (so I can ask for a variable at any time)

"""

__copyright__="""
    narpy - A simple NASA AMES file format Reader for Python
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

import numpy as np
from scipy.interpolate import interp1d

class variable:
    """An object holding the file variables

    Args:
        name (string): name of the variable
        data (list): list of data points

    Attributes:
        name (string): name of the variable
        data (list): list of data points
        dims (int): number of data points
    """    
    def __init__(self,name,data):
        self.name=name
        self.data=data
        self.dims=len(data)
    def __str__(self):
        print(type(self))
        return self.name

class file:
    """An object holding the files content

    Args:
        file_path (string): Path to the .na file

    Attributes:
        author (string): author of the file
        institution (string): intitution that made file
        instrument (string): instrument used to record file data
        project (string): project data was recorded for
        date (string): date of obervations
        xstep (float): Size of intervals in x (0.0 if non-uniform)
        x_units (string): Name of the x variable
        comment (string): file comment/desctiption
        variables (dictionary): dictionary of file variables as varuable objects
    """    
    def __init__(self,file_path):

        with open(file_path,"r") as f:
            raw=f.read().splitlines()

        self.author,self.institution,self.instrument,self.project=raw[1:5]
        self.date,self.xstep,self.x_units=raw[6:9]
        self.xstep=float(self.xstep)

        num_variables=int(raw[9])

        scaling=[float(n) for n in raw[10].split()]
        missing=raw[11].split()
        names=raw[12:12+num_variables]

        if raw[12+num_variables]==0:#According to the dummys guide there should be a 0
            #but according to the examples there shouldn't and both pass their tester
            #http://badc.nerc.ac.uk/cgi-bin/dataex_file.cgi.pl
            del raw[12+num_variables]

        len_header=int(raw[0].split(" ")[0])
        
        self.comment="\n".join(raw[13+num_variables:len_header])
        

        variables={n:[] for n in range(0,num_variables+1)}

        for line in raw[len_header:]:
            line=line.split()
            #variables={k:v.append(line[k]) for k,v in variables.items()} gives None type error everytime
            for k in variables.keys():
                variables[k].append(float(line[k]) if k==0 else float(line[k])*scaling[k-1] if line[k]!=missing[k-1] else np.nan)

        self.variables={names[k-1] if k!=0 else self.x_units:variable(names[k-1] if k!=0 else self.x_units,v) for k,v in variables.items()}

    def __str__(self):
        print(type(self))
        return self.comment
    
    def __getitem__(self,x):
        return self.variables[x]