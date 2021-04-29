import psutil
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import datetime
import time
from threading import Thread
import tkinter as tk

serverName = 'localhost'
registerPort = 3999
dataPort = 0
interval = 0
count = 0
threads = []
clientSocket = socket(AF_INET, SOCK_STREAM)
udpPort = 0
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

    infos = 'CPU: ' +str(temperature_infos['dell_smm'][0][1]) + ' \N{Degree Celsius}'+ '\n\n'
    infos += 'DISK: \nTotal: ' + str(total)+ '\nUSED: ' +str(used) +'\nAvaiable: ' +str(available) + '\nUSED_PERCENT: ' +str(used_percent) +'\n\n'
    infos += 'MEMORY: \nTotal: ' + str(mem_total) + '\nUSED: ' + str(mem_used) + '\nAvaiable: ' + str(mem_avail) +  '\nUSED_PERCENT: '+ str(mem_percent)  
    return infos 


#####################################


def dataConnection():
    global serverName, registerPort, dataPort, interval, clientSocket, count
    
    while True:
        # info = 'Total = ' + str(psutil.virtual_memory().total / pow(2, 30))
        # info += '\nUsed = ' + \
        #     str(psutil.virtual_memory().used / pow(2, 30))
        # info += '\nAvailable = ' + \
        #     str(psutil.virtual_memory().available / pow(2, 30))
        # info += '\nUsed Percent = ' + str(psutil.virtual_memory().percent)
        # info += '\nHas been updated ' + str(count) + ' times\n'
        # count += 1
        info = getInfo()
        try:
            clientSocket.send(info.encode())
        except:
            print("dataSocket close")
            break
        print("Sleep...")
        print('interval in tcp = ' + str(interval))
        time.sleep(interval)


def registerConnection():
    global serverName, registerPort, dataPort, interval, clientSocket, count

    # clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, registerPort))
    message = 'REGISTER\nNAME tinh\nIP 127.0.0.1\nUDP_PORT ' + str(udpPort) + '\nTIME ' + \
        str(datetime.datetime.now()) + '\n'
    clientSocket.send(message.encode())


    message2 = clientSocket.recv(2048).decode()
    interval = int(message2.split()[6])
    dataPort = int(message2.split()[8])
    #check REGISTER RETURN
    #   if .. else
    
    if True:
        clientSocket.send('DATAPORT-RECEIVE\nSTATUS accept'.encode())
    # if False:
        ## sent error to server
        #display wrong protocol.
        # close socket 

    #else 
        #display port number and request client to connect.
        # if cancel, send error to server
        
    #receive DATASOCKET-STATUS. 
        # check protocol
        # if wrong
            #send error to server. close connection (SEND-ERROR)
        # if true

    clientSocket.close()
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, dataPort))
    while True:
        # info = 'Total = ' + str(psutil.virtual_memory().total / pow(2, 30))
        # info += '\nUsed = ' + \
        #     str(psutil.virtual_memory().used / pow(2, 30))
        # info += '\nAvailable = ' + \
        #     str(psutil.virtual_memory().available / pow(2, 30))
        # info += '\nUsed Percent = ' + str(psutil.virtual_memory().percent)
        # info += '\nHas been updated ' + str(count) + ' times\n'
        # count += 1
        
        info = getInfo()
        try:
            clientSocket.send(info.encode())
        except:
            print("dataSocket close")
            break
        print("Sleep...")
        print('interval in tcp = ' + str(interval))
        time.sleep(interval)

    # message3 = clientSocket.recv(2048).decode()
    # status = message3.split()[1]
    # if (status == 'open'):
    #     dataConnection()
    # else:
    #     # server can't open dataPort
    #     print('abc')

    # clientSocket.close()


def udpConnection():
    global serverName, registerPort, dataPort, udpPort, interval, clientSocket, count

    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(('', udpPort))
    while True:
        control, serverAddr = udpSocket.recvfrom(2048)
        #check protocol CHANGE-DATAPORT
            #If fail send error to clent (SEND-ERROR-UDP)
            
            #if true 
        print('receive udp success')
        control = control.decode()
        
        if control.split()[2] == '':
            interval = int(control.split()[4])
        elif control.split()[4] == '':
            dataPort = int(control.split()[2])
        
        else:  
            dataPort = int(control.split()[2])
            interval = int(control.split()[4])
        print('dataPort ' + str(dataPort))
        print('interval in udp = ' + str(interval))

        clientSocket.close()
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, dataPort))
        
        # newThread = Thread(target=dataConnection, args=())
        # newThread.start()
        # threads[0] = newThread
        # while True:
        #     clientSocket.send("hello".encode())
        #     time.sleep(3)


def startClient():
    global udpPort, udpPortEntry
    
    udpPort = int(udpPortEntry.get())

    newThread = Thread(target=registerConnection, args=())
    newThread.start()
    threads.append(newThread)

    newThread2 = Thread(target=udpConnection, args=())
    newThread2.start()
    threads.append(newThread2)




window = tk.Tk()
udpPortEntry = tk.Entry()
udpPortEntry.pack()
udpPortButton = tk.Button(text='Submit', command=startClient)
udpPortButton.pack()
window.mainloop()
