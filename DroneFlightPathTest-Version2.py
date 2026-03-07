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

max_len = 100

z_est_data = deque(maxlen=max_len)
range_data = deque(maxlen=max_len)
vz_data = deque(maxlen=max_len)
edge_data = deque(maxlen=max_len)
x_data = deque(maxlen=max_len)

counter = 0
measured_edge = 0
vz_threshold = 0.4
z_threshold = 0
last_zest = 0


# -------- CALLBACK (NO PLOTTING HERE) --------
def log_callback(timestamp, data, logconf):
    global counter
    global measured_edge
    global last_zest

    z_est = data['stateEstimate.z']
    vz_est = data['stateEstimate.vz']
    range_z = data['range.zrange'] / 1000.0
    
    if abs(vz_est) > vz_threshold:
        measured_edge = measured_edge + (z_est - last_zest)

    if measured_edge < 0.07:
        measured_edge = 0

    
    if measured_edge > 0.2286 and measured_edge < 0.635:
        measured_edge = 0.3048
        
    
    #z_est_data.append(z_est)
    #vz_data.append(vz_est)
    #range_data.append(range_z)
    edge_data.append(measured_edge)

    x_data.append(counter)
    counter += 1
    last_zest = z_est


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI) as scf:
        # Arm the Crazyflie
        # -------- CREATE LOG CONFIG --------
        log_conf = LogConfig(name='ZPosition', period_in_ms=100)

        
        log_conf.add_variable('stateEstimate.z', 'float')
        log_conf.add_variable('stateEstimate.vz', 'float')
        log_conf.add_variable('range.zrange', 'uint16_t')

        scf.cf.log.add_config(log_conf)

        # attach callback
        log_conf.data_received_cb.add_callback(log_callback)

        # start logging
        log_conf.start()

        print("Logging started. Move the drone by hand to observe values.")

        # -------- PLOT SETUP --------
        plt.ion()

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        
        line_edge, = ax1.plot([], [], label="measured_edge")
        #line_z, = ax1.plot([], [], label="z_est")
        #line_range, = ax1.plot([], [], label="range")
        #line_vz, = ax2.plot([], [], label="vz")

        ax1.set_xlabel("Samples")
        ax1.set_ylabel("Height (m)")
        ax2.set_ylabel("Velocity (m/s)")

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        print("Plotting started")

        while True:

            if len(x_data) > 0:

                line_edge.set_data(x_data, edge_data)
                #line_z.set_data(x_data, z_est_data)
                #line_range.set_data(x_data, range_data)
                #line_vz.set_data(x_data, vz_data)

                ax1.set_xlim(max(0, counter - max_len), counter)

                ax1.relim()
                ax1.autoscale_view()

                ax2.relim()
                ax2.autoscale_view()

                plt.draw()
                plt.pause(0.05)

            time.sleep(0.05)
            

        
        
        # Takeoff 
        #with PositionHlCommander(scf, controller=PositionHlCommander.CONTROLLER_PID) as pc:
            
            #time.sleep(1.0)
            #scf.cf.param.set_value('motion.useFlowDisabled', '0')

            #time.sleep(1.0)
            # Go to coordinate]
            #pc.go_to(0.6, 0.0, 0.6)
            #time.sleep(8.0)
            #pc.go_to(0.0, 0.0, 0.6)
            #time.sleep(3.0)
