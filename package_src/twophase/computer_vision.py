# ############################## Start the webserver, the opencv color grabber and the GUI #############################

from threading import Thread
from twophase.vision2 import grab_colors

thr = Thread(target=grab_colors, args=())
thr.start()
# Run the opencv code and detect facelet colors

import twophase.client_gui2
# Start the GUI with several sliders to configure some opencv parameters

# The GUI communicates with the webserver which should listen on the specified port.
