# ############################ Examples how to use the cube solver #####################################################

cubestring = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'  # cube definition string of cube we want to solve
# See module enums.py for the format of the cube definition string

# ######################### Method 1: directly call the solve routine# #################################################
# Advantage: No network layer needed. Disadvantage: Only local usage possible.                                                                  #
########################################################################################################################

#  Uncomment this part if you want to use method 1
"""
import solver as sv
a = sv.solve(cubestring, 20, 2)  # solve with a maximum of 20 moves and a timeout of 2 seconds for example
print(a)
a = sv.solve(cubestring, 18, 5)  # solve with a maximum of 18 moves and a timeout of 5 seconds for example
print(a)
quit()
"""
########################################################################################################################


# ############################### Method 2 a/b: Start the cubesolving-server# ##########################################
# Advantage: Tables have to be loaded only once when the server starts. Disadvantage: Network layer must be present.   #
########################################################################################################################

#----------------------------------------------------------------------------------------------------------------------
# Method 2a: Start the server from inside a Python script:
import start_server
from threading import Thread
background_thread = Thread(target=start_server.start, args=(8080, 20, 2))
background_thread.start()
# Server listens now on port 8080, maxlength 20 moves, timeout 2 seconds
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Method 2b: Start the server from a terminal with parameters for port, maxlength and timeout:
# python start_server.py 8080 20 2
# ----------------------------------------------------------------------------------------------------------------------


# Once the server is started you can transfer the cube definition string to the server with different methods:

# ----------------------------------------------------------------------------------------------------------------------
# 1. With a webbrowser, if the server runs on the same machine on port 8080
# http://localhost:8080/DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL
# With a webbrowser, if the server runs on server myserver.com, port 8081
# http://myserver.com:8081/DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 2. With netcat, if the server runs on the same machine on port 8080
# echo DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL | nc localhost 8080
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# 3. With this little graphical interface.
# From within a Python script start the interface with

import client_gui


# From a terminal start the interface with
# python client_gui.py
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Computer vision

# Start the interface, the server and the webcam from a terminal with

# python computer_vision.py

# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################

