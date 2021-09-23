from datetime import datetime
from _thread import *
import threading
import socket
import time
import sys
from datetime import datetime


def writing():
    while True:
        msg=c_socket.recv(1024)
        print(msg.decode())

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("format: <filename> <server name>")
        sys.exit()
    ser_name = sys.argv[1]
    s_PORT   = 9999
    allhostinfo = socket.getaddrinfo(ser_name, s_PORT)
    # print(allhostinfo)
    hostinfo, _, _ = allhostinfo
    s_host = hostinfo[4]
    #print(s_host)
    if len(s_host) == 2:
        c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c_socket.connect(s_host)
    elif len(s_host) == 4:
        c_socket = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        c_socket.connect((s_host[0],s_host[1],0,0))

    name = input('Enter your name: ')
    c_socket.sendall(name.encode())
    server_name = c_socket.recv(1024)
    server_name = server_name.decode()
    time_now = (datetime.now()).replace(microsecond = 0)
    print('Connected with ',server_name, "at date_time = ", time_now)
    print("\nFormat: >>\"get_list\" for list of clients\n\
        >>\"send all\" sends msg for all\n\
        >>\"send c1 c2 : msg\" sends msg for c1 and c2\n\
        >>\"quit\" for exiting\n")
    start_new_thread(writing,())
    while True:
#        print(server_name,":",message)
        message = input()

        if message =='quit':
            break
        c_socket.send(message.encode())
        # data = c_socket.recv(1024)
        
    c_socket.close()