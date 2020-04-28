import sim
import time
from ur3_api import UR3

ur3_sim = UR3()

ur3_sim.run_coppelia()

joint_values = [1, 0.2, 0.4, -0.8, 0.5, -1] # random position
initial_state = [0, 0, 0, 0, 0, 0]

ur3_sim.joint_values(joint_values)

time.sleep(2)

ur3_sim.joint_values(initial_state)

ur3_sim.stop_simulation()