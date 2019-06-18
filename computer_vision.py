# ############################## Start the webserver, the opencv color grabber and the GUI #############################

import start_server
from threading import Thread
from vision2 import grab_colors
background_thread = Thread(target=start_server.start, args=(8080, 20, 2))
background_thread.start()
# Server listens now on port 8080, maxlength 20 moves, timeout 2 seconds

thr = Thread(target=grab_colors, args=())
thr.start()
# Run the opencv code and detect facelet colors

import client_gui2
# Start the GUI with several sliders to configure some opencv parameters

