import socket
import fmipp
import os
import math
import numpy as np
import time

model_name = 'vs_fmi2'
work_dir = 'C:\\Truck_Sim\\CIDI_sim\\FMU\\blSim'
path_to_fmu = os.path.join(work_dir,model_name + '.fmu')
uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu,work_dir)

logging_on = False
fmu = fmipp.FixedStepSizeFMU( uri_to_extracted_fmu, "vs_fmi2", logging_on )

n_init = 0
init_vars = fmipp.new_string_array( n_init )
init_vals = fmipp.new_double_array( n_init )

# number of outputs
n_outputs = 14

# construct string array with output names
outputs = fmipp.new_string_array( n_outputs )
fmipp.string_array_setitem( outputs, 0, 'Xo' )
fmipp.string_array_setitem( outputs, 1, 'Xo_2' )
fmipp.string_array_setitem( outputs, 2, 'Yo' )
fmipp.string_array_setitem( outputs, 3, 'Yo_2' )
fmipp.string_array_setitem( outputs, 4, 'Yaw' )
fmipp.string_array_setitem( outputs, 5, 'Yaw_2' )
fmipp.string_array_setitem( outputs, 6, 'Pitch' )
fmipp.string_array_setitem( outputs, 7, 'Pitch_2' )
fmipp.string_array_setitem( outputs, 8, 'Roll_E' )
fmipp.string_array_setitem( outputs, 9, 'Roll_E_2' )
fmipp.string_array_setitem( outputs, 10, 'Zo' )
fmipp.string_array_setitem( outputs, 11, 'Zo_2' )
fmipp.string_array_setitem( outputs, 12, 'ZCG_SM' )
fmipp.string_array_setitem( outputs, 13, 'ZCG_SM2' )
fmu.defineRealOutputs( outputs, n_outputs )
print("Got here")

pos_array = np.zeros((14))
#Initializing UDP
print('Initializing UDP socket...')
UDP_IP = "127.0.0.1"
UDP_PORT = 25000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print ('Socket initialized')


start_time = 0.
stop_time = 200.
fmu_step_size = 0.005
sim_step_size = 0.005
t = start_time

status = fmu.init( "blSim_fmi2", init_vars, init_vals, n_init, start_time, fmu_step_size )
assert status == 1


#control looping speed
beginning_of_time = time.perf_counter()
N = 0.005
lt_0 = time.perf_counter()
goAgainAt = lt_0+N

while ( t <= stop_time ):
  fmu.sync( t, t+sim_step_size )  
  t += sim_step_size
  result = fmu.getRealOutputs()
  pos_array[0] = fmipp.double_array_getitem( result, 0)# 'Xo' 
  pos_array[1] = fmipp.double_array_getitem( result, 1)# 'Xo_2' 
  pos_array[2] = fmipp.double_array_getitem( result, 2)# 'Yo' 
  pos_array[3] = fmipp.double_array_getitem( result, 3)# 'Yo_2'
  pos_array[4] = fmipp.double_array_getitem( result, 4)# 'Yaw' 
  pos_array[5] = fmipp.double_array_getitem( result, 5)# 'Yaw_2' 
  pos_array[6] = fmipp.double_array_getitem( result, 6)# 'Pitch' 
  pos_array[7] = fmipp.double_array_getitem( result, 7)# 'Pitch_2' 
  pos_array[8] = fmipp.double_array_getitem( result, 8)# 'Roll_E' 
  pos_array[9] = fmipp.double_array_getitem( result, 9)# 'Roll_E_2' 
  pos_array[10] = fmipp.double_array_getitem( result, 10)# 'Zo' 
  pos_array[11] = fmipp.double_array_getitem( result, 11)# 'Zo_2' 
  pos_array[12] = fmipp.double_array_getitem( result, 12)# 'ZCG_SM' 
  pos_array[13] = fmipp.double_array_getitem( result, 13)# 'ZCG_SM2' 
  msg = pos_array
  sock.sendto(msg,(UDP_IP,UDP_PORT))
  print("sim_time: {}, Loop_time: {}".format(t,time.perf_counter()))
  #if miss itr
  if (time.perf_counter()>goAgainAt):
    print('missed a itr')
    goAgainAt += N
    continue
  #else
  sleep_time = goAgainAt - time.perf_counter()
  goAgainAt += N
  print('sleep_time: {}'.format(sleep_time))
  time.sleep(sleep_time)


  