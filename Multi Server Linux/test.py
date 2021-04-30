import psutil
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import datetime
import time
from threading import Thread
import tkinter as tk
from tkinter import messagebox



clientSocket = socket(AF_INET, SOCK_STREAM)
# change = False

serverName = ''
registerPort = 3999
dataPort = 0
interval = 0
threads = []
udpPort = 0


def getInfo():    
    mem_total = psutil.virtual_memory().total / pow(2, 30)
    mem_used = psutil.virtual_memory().used / pow(2, 30)
    mem_avail = psutil.virtual_memory().available / pow(2, 30)
    mem_percent = psutil.virtual_memory()[2] 
    cDisk = psutil.disk_usage('/')[0]
    dDisk = psutil.disk_usage('/media/sangpham/Goodboy')[0]
    total = (cDisk + dDisk) 
    used = psutil.disk_usage('/')[1] + psutil.disk_usage('/media/sangpham/Goodboy')[1]
    
    available = psutil.disk_usage('/')[2] + psutil.disk_usage('/media/sangpham/Goodboy')[2]

    used_percent = (used / total) * 100

    temperature_infos = psutil.sensors_temperatures();

    infos = 'CPU: ' +str(temperature_infos['coretemp'][0][1]) + ' \N{Degree Celsius}'+ '\n\n'
    infos += 'DISK: \nTotal: ' + str(total)+ '\nUSED: ' +str(used) +'\nAvaiable: ' +str(available) + '\nUSED_PERCENT: ' +str(used_percent) +'\n\n'
    infos += 'MEMORY: \nTotal: ' + str(mem_total) + '\nUSED: ' + str(mem_used) + '\nAvaiable: ' + str(mem_avail) +  '\nUSED_PERCENT: '+ str(mem_percent)  
    return infos 


#####################################



def dataConnection():
    global serverName, registerPort, dataPort, interval, clientSocket
    
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
    global serverName, registerPort, dataPort, interval, clientSocket
    # clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, registerPort))
    name = nameInput.get()
    ip = ipInput.get()
    time1 = '{0:%Y-%m-%d %H:%M}'.format(datetime.datetime.now())
    message = 'REGISTER\nNAME '+ str(name) + '\nIP ' + ip + '\nUDP_PORT ' + str(udpPort) + '\nTIME ' + \
        str(time1) + '\n'
    clientSocket.send(message.encode())


    #recive Register return message
    registerReturn = clientSocket.recv(2048).decode()
    #check REGISTER RETURN (Data )

    if (registerReturn.split()[0].isnumeric()):
        messagebox.showerror("Register Fail", registerReturn)
        clientSocket.close()

        #check missing header
    elif (registerReturn.split()[0] == ''):
        errorMessage = '201 Missing Header'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (registerReturn.split()[2] == ''):
        errorMessage = '201 Missing Status'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (registerReturn.split()[4] == ''):
        errorMessage = '201 Missing ID'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (registerReturn.split()[6] == ''):
        errorMessage = '201 Missing Interval'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (registerReturn.split()[8] == ''):
        errorMessage = '201 Missing Data Port'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

        #check wrong fields
    elif (registerReturn.split()[0] != 'REGISTER-RETURN'):
        errorMessage = '202 Wrong Header'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (registerReturn.split()[2] != 'success' and registerReturn.split()[2] != 'fail'):
        errorMessage = '202 Wrong Status'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()
        
    elif (registerReturn.split()[4].isnumeric() == False):
        errorMessage = '202 Wrong ID'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (int(registerReturn.split()[6]) <= 0):
        errorMessage = '202 Invalid Interval'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()

    elif (int(registerReturn.split()[8]) <= 0 or int(registerReturn.split()[6]) > 65000):
        errorMessage = '202 Invalid Data Port'
        clientSocket.send(errorMessage.encode())
        clientSocket.close()
    # if success
        #display port number and request client to connect.
        # if cancel, send error to server
    elif registerReturn.split()[2] == 'success':
        interval = int(registerReturn.split()[6])
        dataPort = int(registerReturn.split()[8])
        res = messagebox.askyesno('Request', 'Port: '+ str(dataPort) + '\nDo you want to connect to server?') 
        if res == True:
            clientSocket.send('DATAPORT-RECEIVE-RETURN\nSTATUS accept'.encode())
        else:
            clientSocket.send('DATAPORT-RECEIVE-RETURN\nSTATUS deni'.encode())
            clientSocket.close()
    else:
        clientSocket.close()

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
    reciveDatasocketStatus = clientSocket.recv(2048).decode()
    if (reciveDatasocketStatus.split()[0].isnumeric()):
        messagebox.showerror( "DataSocket Fail",reciveDatasocketStatus)
        clientSocket.close()

        #missing header
    elif (reciveDatasocketStatus.split()[0] == ''):
        messagebox.showerror("Error", "401 Missing Header")
    elif (reciveDatasocketStatus.split()[2] == ''):
        messagebox.showerror("Error", "401 Missing Status")
    elif (reciveDatasocketStatus.split()[0]) != 'DATASOCKET-STATUS':
        messagebox.showerror("Error", "402 Wrong Header")
    elif (reciveDatasocketStatus.split()[2]) != 'open':
        messagebox.showerror("Error", "402 Wrong Status")
    elif (reciveDatasocketStatus.split()[2] == 'open'):
        clientSocket.close()
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, dataPort))
        sendData()

    # message3 = clientSocket.recv(2048).decode()
    # status = message3.split()[1]
    # if (status == 'open'):
    #     dataConnection()
    # else:
    #     # server can't open dataPort
    #     print('abc')

    # clientSocket.close()


def udpConnection():
    global serverName, registerPort, dataPort, udpPort, interval, clientSocket

    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(('', udpPort))
    while True:
        control, serverAddr = udpSocket.recvfrom(2048)
        #check protocol CHANGE-DATAPORT
            #If fail send error to clent (SEND-ERROR-UDP)
            #if true
        
        print('receive udp success')
        control = control.decode()
        result = control.split()
        if (result[0] != 'CHANGE-INTERVAL' and result[0] != 'CHANGE-DATAPORT'):
            # udpSocket.sendto('501 Missing Header'.encode(),(serverName, 8000))
            messagebox.showerror("Error", " 501 Missing Header")
        elif (result[0] == 'CHANGE-INTERVAL'):
            if (result[2] == ''):
                # udpSocket.sendto('501 Missing Interval'.encode(),(serverName, 8000))
                messagebox.showerror("Error", " 501 Missing Interval")
            elif (int(result[2]) <= 0):
                # udpSocket.sendto('502 Wrong Interval'.encode(),(serverName, 8000))
                messagebox.showerror("Error", " 502 Wrong Interval")
            else:
                interval = int(result[2])
        elif (result[0] == 'CHANGE-DATAPORT'):
            if (result[2] == ''):
                # udpSocket.sendto('501 Missing Data Port'.encode(),(serverName, 8000))
                messagebox.showerror("Error", " 501 Missing Data Port")
            elif (int(result[2]) <= 0 or int(result[2]) > 65000 ):
                # udpSocket.sendto('501 Wrong Data Port'.encode(),(serverName, 8000))
                messagebox.showerror("Error", " 502 Wrong Data Port")
            else:
                
                # udpSocket.sendto('STATUS success'.encode(),(serverName, 8000))
                # change = True
                # dataPort = int(result[2])
                # time.sleep(5)
                # print('new DataPort ' + str(dataPort))
                # print('interval in udp = ' + str(interval))
                # # sendData()
                # sendDataThread = Thread(target=sendData(), args=())
                # sendDataThread.start()
                
                ### tinh modified ###
                
                dataPort = int(result[2])
                print('new DataPort ' + str(dataPort))
                print('interval in udp = ' + str(interval))
                clientSocket.close()
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverName, dataPort))
                
                ### tinh modified ###


       
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

def sendData():
    # global change
    
    while True:
        # info = 'Total = ' + str(psutil.virtual_memory().total / pow(2, 30))
        # info += '\nUsed = ' + \
        #     str(psutil.virtual_memory().used / pow(2, 30))
        # info += '\nAvailable = ' + \
        #     str(psutil.virtual_memory().available / pow(2, 30))
        # info += '\nUsed Percent = ' + str(psutil.virtual_memory().percent)
        # info += '\nHas been updated ' + str(count) + ' times\n'
        # count += 1
        # if change == True:
        #     clientSocket.close()
        #     break
        info = getInfo()
        # if change == True:
        #     clientSocket.close()
        #     change = False
        #     break
        try:
            clientSocket.send(info.encode())
        except:
            clientSocket.close()
            print("dataSocket close")
        
        print("Sleep...")
        print('interval in tcp = ' + str(interval))
        time.sleep(interval)
    
def setServerIp():
    global serverName
    serverName = serverIP.get()
    messagebox.showinfo("Success","Done!")


window = tk.Tk()


ipServerLabel = tk.Label(text='Server IP: ')
ipServerLabel.pack()

serverIP = tk.Entry()
serverIP.pack()

setIpButton = tk.Button(text="Apply", command=setServerIp)
setIpButton.pack()
udpLabel = tk.Label(text='UDP: ')
udpLabel.pack()

udpPortEntry = tk.Entry()
udpPortEntry.pack()


nameLabel = tk.Label(text='Name: ')
nameLabel.pack()

nameInput = tk.Entry()
nameInput.pack()

ipLabel = tk.Label(text='IP: ')
ipLabel.pack()

ipInput = tk.Entry()
ipInput.pack()


udpPortButton = tk.Button(text='Submit', command=startClient)
udpPortButton.pack()



window.mainloop()
