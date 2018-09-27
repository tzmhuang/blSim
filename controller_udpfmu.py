import socket
import fmipp
import os
import math
import numpy as np
import time

# work_dir = 'C:\\Truck_Sim\\CIDI_sim\\FMU'
# model_name = 'blSim'
work_dir = 'C:\\Truck_Sim\\CIDI_sim\\FMU'
model_name = 'blSim'
path_to_fmu = os.path.join(work_dir,model_name + '.fmu')

uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu,work_dir)

# logging_on = False
# fmu = fmipp.FixedStepSizeFMU(uri_to_extracted_fmu,model_name,logging_on)

# n_init = 0

# init_vals = fmipp.new_double_array( n_init )
# fmipp.double_array_setitem( init_vals, 0, 0.1 * math.pi )

# n_outputs = 1
# outputs = fmipp.new_string_array(n_outputs)
# fmipp.string_array_setitem( outputs, 0, 'Xo' )
# # fmipp.string_array_setitem( outputs, 1, 'Xo_2' )
# # fmipp.string_array_setitem( outputs, 2, 'Yo' )
# # fmipp.string_array_setitem( outputs, 3, 'Yo_2' )
# # fmipp.string_array_setitem( outputs, 4, 'Yaw' )
# # fmipp.string_array_setitem( outputs, 5, 'Yaw_2' )
# # fmipp.string_array_setitem( outputs, 6, 'Pitch' )
# # fmipp.string_array_setitem( outputs, 7, 'Pitch_2' )
# # fmipp.string_array_setitem( outputs, 8, 'Roll_E' )
# # fmipp.string_array_setitem( outputs, 9, 'Roll_E_2' )
# # fmipp.string_array_setitem( outputs, 10, 'Zo' )
# # fmipp.string_array_setitem( outputs, 11, 'Zo_2' )
# # fmipp.string_array_setitem( outputs, 12, 'ZCG_SM' )
# # fmipp.string_array_setitem( outputs, 13, 'ZCG_SM2' )
# print('1')
# fmu.defineRealOutputs(outputs, 1)
# print('2')

# start_time = 0.
# stop_time = 100.
# fmu_step_size = 0.001
# sim_step_size = 0.001
# time = start_time

# status = fmu.init( "blSim", None, init_vals, n_init, start_time, fmu_step_size )
# assert status == 1

# while (time<=stop_time):
#     fmu.sync(time,time + sim_step_size)
#     time+=sim_step_size
#     result = fmu.getRealOutputs()
#     print(time)


logging_on = False
fmu = fmipp.FixedStepSizeFMU( uri_to_extracted_fmu, "blSim", logging_on )

# number of parameter to be initialzed
n_init = 1

# construct string array for init parameter names
init_vars = fmipp.new_string_array( n_init )
fmipp.string_array_setitem( init_vars, 0, 'omega' )

# construct double array for init parameter values
init_vals = fmipp.new_double_array( n_init )
fmipp.double_array_setitem( init_vals, 0, 0.1 * math.pi )

# number of outputs
n_outputs = 1

# construct string array with output names
outputs = fmipp.new_string_array( n_outputs )
fmipp.string_array_setitem(outputs,0,'Xo')

# define real output names
fmu.defineRealOutputs( outputs, n_outputs )
print(1)

start_time = 0.
stop_time = 5.
fmu_step_size = 1. # fixed step size enforced by FMU
sim_step_size = 0.2 # step size of simulation
time = start_time

status = fmu.init( "test_sine", init_vars, init_vals, n_init, start_time, fmu_step_size )
assert status == 1

while ( time <= stop_time ):
  fmu.sync( time, time + sim_step_size )
  time += sim_step_size
  result = fmu.getRealOutputs()