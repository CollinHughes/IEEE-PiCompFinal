#!/home/collin/Desktop/DroneFlight/.venv/bin/python
# ----------------------------------------------------------------------
# Heavy work in progress
# ----------------------------------------------------------------------
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig

import matplotlib.pyplot as plt
from collections import deque


#URI = 'radio://0/80/250K'
URI = 'radio://0/80/2M'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

measured_edge = 0.0
vz_threshold = 0.08
last_zest = 0.0

launch_s = 3
forward_s = 8 + launch_s
home_s = 4 + forward_s

y_dist = 0.0
x_dist = 0.0


# -------- CALLBACK (NO PLOTTING HERE) --------
def log_callback(timestamp, data, logconf):
    global measured_edge
    global last_zest
    global x_dist
    global y_dist

    z_est = data['stateEstimate.z']
    y_dist = data['stateEstimate.y']
    x_dist = data['stateEstimate.x']
    vz_est = data['stateEstimate.vz']
    
    if abs(vz_est) > vz_threshold:
        measured_edge = measured_edge + (z_est - last_zest)

    if measured_edge < 0.07:
        measured_edge = 0

    
    if measured_edge > 0.2286 and measured_edge < 0.635:
        measured_edge = 0.3048
        
    last_zest = z_est
    


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)
    
    launch_once = 0
    forward_once = 0
    home_once = 0
    last_edge = 0.0
    with SyncCrazyflie(URI) as scf:
        # Arm the Crazyflie
        # CONFIG LOG ---------------------------------------------------
        log_conf = LogConfig(name='Creature', period_in_ms=100)
        
        log_conf.add_variable('stateEstimate.z', 'float')
        log_conf.add_variable('stateEstimate.y', 'float')
        log_conf.add_variable('stateEstimate.x', 'float')
        log_conf.add_variable('stateEstimate.vz', 'float')

        scf.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(log_callback)
        log_conf.start()

        #Takeoff 
        with PositionHlCommander(scf, controller=PositionHlCommander.CONTROLLER_PID) as pc:
        #while True:
            edge = measured_edge
            last_edge = edge
            

            for i in range(home_s*20): #20*seconds (3)
                time.sleep(0.05)
                last_edge = edge
                edge = measured_edge
                if i < (launch_s*20):
                    #if (launch_once == 0) or (last_edge != edge):
                    #    pc.go_to(0.0, 0.0, (0.6 + edge)) 
                    launch_once = 1
                    measured_edge = 0.0
                    edge = 0.0
                    last_edge = 0.0
                elif i < (forward_s*20):
                    if (forward_once == 0) or (last_edge != edge):
                        pc.go_to(0.6, 0.0, (0.6 + edge))
                        forward_once = 1
                elif i >= (forward_s*20):
                    if (home_once == 0) or (last_edge != edge):
                        pc.go_to(0.0, 0.0, (0.6 + edge))
                        home_once = 1
                print("X/Y", edge, " ", x_dist, " ", y_dist)
                # If the distance is too high, end the for loop
                if (measured_edge >= 0.635) or (abs(y_dist) > 0.381) or (x_dist < -0.381) or (x_dist > 0.854):
                    break

            
