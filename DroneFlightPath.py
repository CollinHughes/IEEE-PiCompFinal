#!/home/collin/Desktop/CompPiProgram/.venv/bin/python
# ----------------------------------------------------------------------
# Heavy work in progress
# ----------------------------------------------------------------------


import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.position_hl_commander import PositionHlCommander
from cflib.crazyflie.log import LogConfig
# ----------------------------------------------------------------------
# Drone 
# ----------------------------------------------------------------------
#URI = 'radio://0/80/250K'
def fly_drone():
    print("Flight Starting")
    try:
        URI = 'radio://0/80/2M'

        logging.basicConfig(level=logging.ERROR)
        launch_s = 3
        forward_s = 5 + launch_s
        approach_s = 3 + forward_s
        home_s = 3 + approach_s

        y_dist = 0.0
        x_dist = 0.0
        z_dist = 0.0

        def log_callback(timestamp, data, logconf):
            global z_dist
            global x_dist
            global y_dist

            z_dist = data['stateEstimate.z']
            y_dist = data['stateEstimate.y']
            x_dist = data['stateEstimate.x']
            

            
            # Initialize the low-level drivers (don't list the debug drivers)
        cflib.crtp.init_drivers(enable_debug_driver=False)
        if True:
            with SyncCrazyflie(URI) as scf:
                # Arm the Crazyflie
                # CONFIG LOG ---------------------------------------------------
                log_conf = LogConfig(name='Creature', period_in_ms=100)
                
                log_conf.add_variable('stateEstimate.z', 'float')
                log_conf.add_variable('stateEstimate.y', 'float')
                log_conf.add_variable('stateEstimate.x', 'float')

                scf.cf.log.add_config(log_conf)
                log_conf.data_received_cb.add_callback(log_callback)
                log_conf.start()

                #Takeoff 
                if (x_dist < 0.0762) and (y_dist < 0.0762):
                    with PositionHlCommander(scf, controller=PositionHlCommander.CONTROLLER_PID) as pc:
                        for i in range(home_s*20):
                            if i == (20*launch_s):       
                                pc.go_to(0.6, 0.0, 0.7112)
                            if i == (20*forward_s):
                                pc.go_to(-0.0254, 0.0, 0.6)
                            if i == (20*approach_s):
                                pc.go_to(0.0, 0.0, 0.4)

                            # If the distance is too high, end the for loop
                            if (z_dist > 1.3) or (abs(y_dist) > 0.381) or (x_dist < -0.381) or (x_dist > 0.854):
                                break
                            time.sleep(0.05)
    except SystemExit as e:
        print("[WARN] Prevented system exit:", e)

