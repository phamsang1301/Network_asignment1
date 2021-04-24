import psutil
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import datetime
import time
from threading import Thread
import pickle

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
    timenow =  str(datetime.datetime.now())
    msg = {'IP': "127.0.0.1", 'NAME': "Sang", 'UDP_PORT': 4001, 'TIME':timenow  }
    message = pickle.dumps(msg)
    clientSocket.send(message)
    # open_udp_connection()
    

    recive_msg_from_server = clientSocket.recv(1024)
    m2 =  pickle.loads(recive_msg_from_server)
    ## if success, sent computer info to server
    if (m2['STATUS'] == "Success"):
        interval = int(m2['INTERVAL'])
        serverPort = int(m2['TCP_PORT'])
        
        while(True):
            print(getInfo())
            send_infos = pickle.dumps(getInfo())
            
            clientSocket.send(send_infos)
            print("Sleep...")
            print('interval in tcp = ' + str(interval))
            time.sleep(interval)
        
            
    
    
def open_udp_connection():
    global interval
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind((serverName, 4001))
    control = '';
    while True:
        control, serverAddr = udpSocket.recvfrom(1024)
        if (control != ''):
                
            print('receive udp success')
            ctrl = pickle.loads(control)
            serverPort = ctrl['TCP_PORT']
            interval = ctrl['INTERVAL']
            print('Changed parameter!')
            print('New Interval: ' + str(interval))
            print('serverPort: ' + str(serverPort))
        control = '';
        
threads = []

# newThread = Thread(target=open_tcp_connection, args=())
# newThread.start()
# threads.append(newThread)        
    

if __name__ == "__main__":
    open_tcp_connection()
    
                



    