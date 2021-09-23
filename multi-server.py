from _thread import *
from datetime import datetime
import threading
import socket
import time
import sys
from datetime import datetime

MAX_CLIENTS = 10
client_list=[]
client_names=[]
tabs = "\t\t\t\t\t"

#my_lock = threading.Lock() 

# def time_now()
#     timenow = datetime.now()

def threaded(conn,name):
    while True:
        message = conn.recv(1024)
        time_now = str(datetime.now().replace(microsecond = 0))
        if not message:
            print(name+" connection closed")
            break
        command=message.decode().split()
        if command[0]=="get_list":
            msg = tabs + time_now + '\n' + tabs + "Available client: "+" ".join(client_names)
            msg=msg.encode()
            conn.send(msg)
        elif command[0]=="send" and command[1]=="all" and len(command)>=3:
            for (names,connec) in client_list:
                if connec != conn:
                    msg= tabs + time_now + '\n' + tabs + name+" (broadcasted) : "+" ".join(command[2:])
                    connec.send(msg.encode())
        elif command[0]=="send":
            div=command.index(":")
            list_of_c=command[1:div]
            if div == 2:
                msg= tabs + time_now + '\n' + tabs + name+" (singlecasted) : "+" ".join(command[div+1:])
            else:
                msg= tabs + time_now + '\n' + tabs + name+" (multicasted) : "+" ".join(command[div+1:])
            for (names,connec) in client_list:
                if names in list_of_c:
                    connec.send(msg.encode())
    conn.close()
    client_list.remove((name,conn))
    client_names.remove(name)
#    my_lock.release()

if __name__ == '__main__':

    s_soc = socket.socket(socket.AF_INET6,type=socket.SOCK_STREAM)  # creating socket
    port = 9999

    s_soc.bind((b'',port,0,0)) #binding host to port #s_hostname
    #print("IP of server :",s_ip)

    name = input('Enter name of Server:')
    s_soc.listen(MAX_CLIENTS)
    time_now = (datetime.now()).replace(microsecond = 0)
    print("server starting at date_time = ", time_now)
    while True:
#        my_lock.acquire()
        conn, add = s_soc.accept() # accepting connection 
        
        c_message = conn.recv(1024)
        name_of_client=c_message.decode()
        print("Name of client: ",name_of_client)
        client_list.append((name_of_client,conn))
        client_names.append(name_of_client)
        conn.send(name.encode())
        start_new_thread(threaded, (conn,name_of_client))
    s_soc.close()