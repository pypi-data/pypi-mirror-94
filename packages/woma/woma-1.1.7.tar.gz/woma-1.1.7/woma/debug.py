#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:13:55 2021

@author: sergio
"""
import woma
from importlib import reload
import sys
import numpy as np

R_earth = 6.371e6  # m
M_earth = 5.9724e24  # kg m^-3

# %%
woma.load_eos_tables()
print(woma.misc.utils.check_loaded_eos_tables())


#%%
if True:
    woma.load_eos_tables()
    #for k, v in sys.modules.items():
    #        if k == 'woma':
    #            reload(v)
print(woma.misc.utils.check_loaded_eos_tables())
print(woma.eos.sesame.T_rho_s(10000, 4000, 305))

#%%

planet = woma.Planet(
    name            = "hello_world",
    A1_mat_layer    = ["ANEOS_Fe85Si15", "ANEOS_forsterite"],
    A1_T_rho_type   = ["entropy=1500", "adiabatic"],
    P_s             = 1e5,
    T_s             = 1000,
)

planet.M = M_earth
planet.R = R_earth

# Generate the profiles
planet.gen_prof_L2_find_R1_given_M_R()
print(woma.misc.utils.check_loaded_eos_tables())

#%%
planet = woma.Planet(
    A1_mat_layer    = ["Til_iron", "SESAME_basalt"],
    A1_T_rho_type   = ["power=0.5", "adiabatic"],
    P_s             = 1e5,
    T_s             = 1000,
    A1_M_layer      = [0.3 * M_earth, 0.7 * M_earth],
)

print(woma.misc.utils.check_loaded_eos_tables())
#%%
# Generate the profiles
planet.gen_prof_L2_find_R_R1_given_M1_M2(R_min=0.9 * R_earth, R_max=1.05 * R_earth)

#%%
print(woma.misc.utils.check_loaded_eos_tables())

for mat_id in range(300, 308):
    try:
        print(woma.eos.sesame.T_rho_s(2868.000001763966,1760.5805608495987,mat_id))
    except:
        print(mat_id, "not available")
        
for mat_id in range(400, 403):
    try:
        print(woma.eos.sesame.T_rho_s(2868.000001763966,1760.5805608495987,mat_id))
    except:
        print(mat_id, "not available")
print(woma.misc.utils.check_loaded_eos_tables())

#%%
print(woma.eos.sesame.T_rho_s(10000, 4000, 301))
print(woma.eos.T_rho.T_rho(5000, 2, [1e4,], 301))
#%%
for k, v in sys.modules.items():
        if (
            k.startswith("woma")
        ):
            print(v)