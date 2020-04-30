import sys
sys.path.insert(1, 'src')

import sim
from ur3_api import UR3

import time
import random

ur3_sim = UR3()

ur3_sim.run_coppelia()

initial_state = [0, 0, 0, 0, 0, 0]

for i in range (5):
    random.seed(i)
    joint_values = [random.random(), random.random(), random.random(), 
                    random.random(), random.random(), random.random()]

    ur3_sim.joint_values(joint_values)
    time.sleep(1)

    ur3_sim.joint_values(initial_state)
    time.sleep(1)

ur3_sim.stop_simulation()
