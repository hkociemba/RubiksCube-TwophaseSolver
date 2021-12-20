# ##################################### Start the webserver ############################################################

import twophase.start_server as start_server
from threading import Thread


def start(port, maxlength, timeout):
    background_thread = Thread(target=start_server.start, args=(port, maxlength, timeout))
    background_thread.start()
