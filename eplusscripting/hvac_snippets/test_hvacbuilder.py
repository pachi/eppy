# Copyright (c) 2012 Santosh Phillip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""py.test for hvacbuilder"""
import sys
import os
sys.path.append('../')
import hvacbuilder
from modeleditor import IDF
import random
from StringIO import StringIO

# idd is read only once in this test
from iddcurrent import iddcurrent
iddfhandle = StringIO(iddcurrent.iddtxt)
IDF.setiddname(iddfhandle)


def test_flattencopy():
    """py.test for flattencopy"""
    tdata = (([1,2], [1,2]), #lst , nlst
    ([1,2,[3,4]], [1,2,3,4]), #lst , nlst
    ([1,2,[3,[4,5,6],7,8]], [1,2,3,4,5,6,7,8]), #lst , nlst
    ([1,2,[3,[4,5,[6,7],8],9]], [1,2,3,4,5,6,7,8,9]), #lst , nlst
    )
    for lst , nlst in tdata:
        result = hvacbuilder.flattencopy(lst)
        assert result == nlst

def test_makeplantloop():
    """pytest for makeplantloop"""
    tdata = (("", 
    "p_loop",
    ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'],
    ['db0', ['db1', 'db2', 'db3'], 'db4'],
    """BRANCH, sb0, 0, , Pipe:Adiabatic, sb0_pipe, p_loop Supply Inlet, sb0_pipe_outlet, Bypass;BRANCH, sb1, 0, , Pipe:Adiabatic, sb1_pipe, sb1_pipe_inlet, sb1_pipe_outlet, Bypass;BRANCH, sb2, 0, , Pipe:Adiabatic, sb2_pipe, sb2_pipe_inlet, sb2_pipe_outlet, Bypass;BRANCH, sb3, 0, , Pipe:Adiabatic, sb3_pipe, sb3_pipe_inlet, sb3_pipe_outlet, Bypass;BRANCH, sb4, 0, , Pipe:Adiabatic, sb4_pipe, sb4_pipe_inlet, p_loop Supply Outlet, Bypass;BRANCH, db0, 0, , Pipe:Adiabatic, db0_pipe, p_loop Demand Inlet, db0_pipe_outlet, Bypass;BRANCH, db1, 0, , Pipe:Adiabatic, db1_pipe, db1_pipe_inlet, db1_pipe_outlet, Bypass;BRANCH, db2, 0, , Pipe:Adiabatic, db2_pipe, db2_pipe_inlet, db2_pipe_outlet, Bypass;BRANCH, db3, 0, , Pipe:Adiabatic, db3_pipe, db3_pipe_inlet, db3_pipe_outlet, Bypass;BRANCH, db4, 0, , Pipe:Adiabatic, db4_pipe, db4_pipe_inlet, p_loop Demand Outlet, Bypass;BRANCHLIST, p_loop Supply Branchs, sb1, sb2, sb3;BRANCHLIST, p_loop Demand Branchs, db1, db2, db3;CONNECTOR:SPLITTER, p_loop_supply_splitter, sb0, sb1, sb2, sb3;CONNECTOR:SPLITTER, p_loop_demand_splitter, db0, db1, db2, db3;CONNECTOR:MIXER, p_loop_supply_mixer, sb4, sb1, sb2, sb3;CONNECTOR:MIXER, p_loop_demand_mixer, db4, db1, db2, db3;CONNECTORLIST, p_loop Supply Connectors, Connector:Splitter, p_loop_supply_splitter, Connector:Mixer, p_loop_supply_mixer;CONNECTORLIST, p_loop Demand Connectors, Connector:Splitter, p_loop_demand_splitter, Connector:Mixer, p_loop_demand_mixer;PIPE:ADIABATIC, sb0_pipe, p_loop Supply Inlet, sb0_pipe_outlet;PIPE:ADIABATIC, sb1_pipe, sb1_pipe_inlet, sb1_pipe_outlet;PIPE:ADIABATIC, sb2_pipe, sb2_pipe_inlet, sb2_pipe_outlet;PIPE:ADIABATIC, sb3_pipe, sb3_pipe_inlet, sb3_pipe_outlet;PIPE:ADIABATIC, sb4_pipe, sb4_pipe_inlet, p_loop Supply Outlet;PIPE:ADIABATIC, db0_pipe, p_loop Demand Inlet, db0_pipe_outlet;PIPE:ADIABATIC, db1_pipe, db1_pipe_inlet, db1_pipe_outlet;PIPE:ADIABATIC, db2_pipe, db2_pipe_inlet, db2_pipe_outlet;PIPE:ADIABATIC, db3_pipe, db3_pipe_inlet, db3_pipe_outlet;PIPE:ADIABATIC, db4_pipe, db4_pipe_inlet, p_loop Demand Outlet;PLANTLOOP, p_loop, Water, , , , , , , 0.0, Autocalculate, p_loop Supply Inlet, p_loop Supply Outlet, p_loop Supply Branchs, p_loop Supply Connectors, p_loop Demand Inlet, p_loop Demand Outlet, p_loop Demand Branchs, p_loop Demand Connectors, Sequential, , SingleSetpoint, None, None;"""
    ), # blankidf, loopname, sloop, dloop, nidf
    )
    for blankidf, loopname, sloop, dloop, nidf in tdata:
        
        fhandle = StringIO("")
        idf1 = IDF(fhandle)
        loopname = "p_loop"
        sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
        dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
        hvacbuilder.makeplantloop(idf1, loopname, sloop, dloop)
        idf2 = IDF(StringIO(nidf))
        assert str(idf1.model) == str(idf2.model)