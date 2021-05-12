import psutil
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import datetime
import time
from threading import Thread
import pickle
import tkinter as tk

# for sensor in temperature_infos:
#     print(sensor)

# print(temperature_infos['dell_smm'][0])
print("-----------------")
# print(psutil.virtual_memory())


# print('Total = ' + str(psutil.virtual_memory().total / pow(2, 30)))
# print('Used = ' + str(psutil.virtual_memory().used / pow(2, 30)))
# print('Available = ' + str(psutil.virtual_memory().available / pow(2, 30)))
# print('Used Percent = ' + str(psutil.virtual_memory().percent))
# print("-----------------")

# print(cDisk)
# print(dDisk)
# print('Total = ' + str((cDisk.total + dDisk.total) / pow(2, 30)))
# print('Used = ' + str((cDisk.used + dDisk.used) / pow(2, 30)))
# print('Available = ' + str((cDisk.free + dDisk.free) / pow(2, 30)))
# print('Used Percent = ' + str((cDisk.used + dDisk.used) /
#                               (cDisk.total + dDisk.total) * 100))

def getInfo():    
    mem_total = psutil.virtual_memory().total / pow(2, 30)
    mem_used = psutil.virtual_memory().used / pow(2, 30)
    mem_avail = psutil.virtual_memory().available / pow(2, 30)
    mem_percent = psutil.virtual_memory()[2] 
    cDisk = psutil.disk_usage('/')[0]
    dDisk = psutil.disk_usage('/media/sangpham/GoodBoy')[0]
    total = (cDisk + dDisk) 
    used = psutil.disk_usage('/')[1] + psutil.disk_usage('/media/sangpham/GoodBoy')[1]
    
    available = psutil.disk_usage('/')[2] + psutil.disk_usage('/media/sangpham/GoodBoy')[2]
     
    used_percent = (used / total) * 100

    temperature_infos = psutil.sensors_temperatures();
    infos = {'CPU': temperature_infos['dell_smm'][0][1], 'DISK': {'Total': total, 'USED': used,'Avaiable': available, 'USED_PERCENT': used_percent },'MEMORY':{'Total': mem_total, 'USED': mem_used,'Avaiable': mem_avail, 'USED_PERCENT': mem_percent } }

    return infos

####################################################################33
serverName = 'localhost'
serverPort = 4000
interval = 0


def open_tcp_connection():
    global serverName, serverPort, interval 
    clientSocket = socket(AF_INET, SOCK_STREAM)    # open 
    clientSocket.connect((serverName, serverPort))  # connection
    
    #sent info client to server
    # msg = {'IP': "127.0.0.1", 'NAME': "Sang", 'UDP_PORT': 4001, 'TIME':timenow }
    msg = "NAME: Sang\nIP: 127.0.0.1\nUDP_PORT: 4002\nTIME: " + \
        str(datetime.datetime.now()) + "\n"
        
    clientSocket.send(msg.encode())
    

    recive_msg_from_server = clientSocket.recv(
        2048).decode()
    # m2 =  pickle.loads(recive_msg_from_server)

    ## if success, sent computer info to server
    if (recive_msg_from_server.split()[1] == "Success"):
        interval = int(recive_msg_from_server.split()[5])
        serverPort = int(recive_msg_from_server.split()[7])
    
        while(True):
            print(getInfo())
            send_infos = pickle.dumps(getInfo())
            clientSocket.send(send_infos)
            print("Sleep...")
            print('Interval in tcp = ' + str(interval))
            time.sleep(interval)
    # if fail, sent again
        ##  do
        ##  something 
        ##   here
           

    


def udpConnection():
    global interval
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(('', 4002))
    while True:
        control, serverAddr = udpSocket.recvfrom(2048)
        print('receive udp success')
        # control = control.decode()
        # serverPort = int(control.split()[1])
        # interval = int(control.split()[3])
        d = pickle.loads(control)
        if d['port'] == '':
            interval = int(d['interval'])
        elif d['interval'] == '':
            d['port'] = int(d['port'])
        
        else:
            serverPort = int(d['port'])
            interval = int(d['interval'])

        print('receive udp success 2')
        print('Interval in udp = ' + str(interval))

threads = []

newThread = Thread(target=open_tcp_connection, args=())
newThread.start()
threads.append(newThread)        

newThread1  = Thread(target=udpConnection(), args=())
newThread1.start()
threads.append(newThread1)

window = tk.Tk()
window.title("Client")

label = tk.Label(text="IP: ")
window.columnconfigure(id, weight=1)

window.mainloop()
    
                



    