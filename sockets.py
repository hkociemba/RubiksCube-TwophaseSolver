# ################## The code of the server socket which communicates with the client ##################################

import socket
import sys
import threading
import solver
import time


def client_thread(conn, maxlen, timeout):
    while True:  # infinite loop only necessary for telnet client
        # Receiving from client
        data = []
        while not (ord('\n') in data or ord('\r') in data):
            try:
                a = conn.recv(1024).upper()
                if len(a) == 0:
                    conn.close()
                    print('Connection closed', flush=True)
                    return
            except:
                print('Connection closed', flush=True)
                conn.close()
                return
            for i in range(len(a)):
                if a[i] in [ord('\n'), ord('\r'), ord('G'), ord('E'), ord('T'),  ord('U'), ord('R'), ord('F'), ord('D'),
                            ord('L'), ord('B')]:
                    data.append(a[i])
        if data[0] == ord('X'):
            break
        defstr = ''.join(chr(i) for i in data if chr(i) > chr(32))
        qpos = defstr.find('GET')
        if qpos >= 0:  # in this case we suppose the client is a webbrowser
            defstr = defstr[qpos+3:qpos+57]
            reply = 'HTTP/1.1 200 OK' + '\n\n' + '<html><head><title>Answer from Cubesolver</title></head><body>' + '\n'
            reply += solver.solve(defstr, maxlen, timeout) + '\n' + '</body></html>' + '\n'
            conn.sendall(reply.encode())
            conn.close()
        else:  # other client, for example the GUI client or telnet
            reply = (solver.solve(defstr, maxlen, timeout)+'\n').encode()
            print(defstr)
            try:
                conn.sendall(reply)
            except:
                print('Error while sending data. Connection closed', flush=True)
                conn.close()
                return
    conn.close()


def server_start(args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server socket created')
    try:
        s.bind(('', int(args[1])))  # bind socket to local host and port
    except socket.error as e:
        print('Server socket bind failed. Error Code : ' + str(e.errno))
        sys.exit()
    s.listen(10)
    print('Server now listening...')

    while 1:
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]) + ', ' + time.strftime("%Y.%m.%d  %H:%M:%S"))
        threading.Thread(target=client_thread, args=(conn, int(args[2]), int(args[3]))).start()
    s.close()

