# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time

class UR3:

    def __init__(self, clientID=None, joints=None):
        self.clientID = clientID
        self.joints = joints

    def run_coppelia(self):

        print ('Program started')
        sim.simxFinish(-1) # just in case, close all opened connections
        self.clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
        if self.clientID!=-1:
            print ('Connected to remote API server')

            # Now try to retrieve data in a blocking fashion (i.e. a service call):
            res,objs=sim.simxGetObjects(self.clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
            if res==sim.simx_return_ok:
                print ('Number of objects in the scene: ',len(objs))
            else:
                print ('Remote API function call returned with error code: ',res)

            time.sleep(2)

            robot_name = 'UR3'

            errorCodes, self.joints = [], []
            
            for i in range (1, 7):
                errorCode, joint = sim.simxGetObjectHandle(self.clientID, robot_name + '_joint' + str(i), sim.simx_opmode_oneshot_wait)
                errorCodes += [errorCode]
                self.joints += [joint]
            
            if -1 in errorCodes:
                print ("Erro na criação de Handles")

            return (self.clientID, self.joints)

        else:
            print ('Failed connecting to remote API server')

    def joint_values(self, thetas):

        joint_values = thetas
        # Atualizamos o valor de cada junta no Coppelia
        errorCodes = []
        for joint, joint_value in zip(self.joints, joint_values):
            errorCodes += [sim.simxSetJointTargetPosition(self.clientID, joint, joint_value, sim.simx_opmode_oneshot)]
            
            if -1 in errorCodes:
                print ("Erro na definição de target para posicao")
            
            time.sleep(0.05)

    def stop_simulation(self):

        # Now send some data to CoppeliaSim in a non-blocking fashion:
        sim.simxAddStatusbarMessage(self.clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

        # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
        sim.simxGetPingTime(self.clientID)

        # Now close the connection to CoppeliaSim:
        sim.simxFinish(self.clientID)
