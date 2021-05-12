from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import time
import tkinter as tk
from functools import partial
from tkinter import messagebox  
from tkinter import ttk
import datetime
change = False


# def hasNumbers(inputString):
#     return any(char.isdigit() for char in inputString)
# def checkip_type(ip):
#     	ip_tmp = ip.split('.')
# 	if len(ip_tmp) != 4:
# 		return False
 
# 	for x in ip_tmp:
# 		if not x.isdigit():
# 			return False
# 		i = int(x)
# 		if i < 0 or i > 255:
# 			return False
# 	return True
def checkIp(ip):
    temp = ip.split('.')
    if len(temp) != 4:
        return False
    for x in temp:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True
def changeTcpPort(udpPort, clientIP, id,clientName, registerTime):
    global changeTcpPortInputs, change
    newDataPort = changeTcpPortInputs[id].get()
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    control = 'CHANGE-DATAPORT\nNEW-DATAPORT ' + newDataPort +'\n'
    udpSocket.sendto(control.encode(), (clientIP, udpPort))
    # messagebox.showinfo("Success", "Sent!")

    #recieve protocol (SEND-ERROR-UDP)
        # if fail 
            # display error on clinet's screen
        # if true 
    if (newDataPort.isnumeric()):
        change = True

        newDataPort = int(changeTcpPortInputs[id].get())
        newServer = socket(AF_INET, SOCK_STREAM)
        newServer.bind(('', newDataPort))
        newServer.listen(40)
            
            # while True:
            #modify in client -- if status = open
            # registerSocket.send('STATUS open\n'.encode())
        newDataSocket2, addr = newServer.accept()
        newThread = Thread(target=dataConnection2, args=(
            newServer, newDataSocket2, newDataPort, id,clientName, clientIP,registerTime))
        newThread.start()
    
def sendInterval(udpPort, clientIP, id):
    global changeIntervalInputs
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    control = 'CHANGE-INTERVAL\nINTERVAL ' + changeIntervalInputs[id].get() +'\n'
    udpSocket.sendto(control.encode(), (clientIP, udpPort))
    # messagebox.showinfo("Success", "Sent!")
    # control, clientIP = udpSocket.recvfrom(2048)
    # control = control.decode()
    # result = control.split()
    # if (result[0] != 'STATUS'):
    #     messagebox.showerror("error",control)
    


def dataConnection2(server, dataSocket2, dataPort, id,clientName, clientIP, registerTime):
    # newLabel = tk.Label(text='client ' + str(id) +
    #                     '\ndataPort ' + str(dataPort) + '\n')
    # labels.append(newLabel)
    # newLabel.grid(row=0, column=id)

    # changeTcpPortInput = tk.Entry()
    # changeTcpPortInputs.append(changeTcpPortInput)
    # changeTcpPortInputs[id].grid(row=1, column=id)
    # changeTcpPortButton = tk.Button(
    #     text='Change TCP Port', command=changeTcpPort(id))
    # changeTcpPortButton.grid(row=2, column=id)

    # window.columnconfigure(id, weight=1)
    
    time.sleep(1)  # time to stop receiving info from previous dataPort
    global change
    while True:
        if change == True:
            # close socket
            dataSocket2.close()
            server.close()
            print ('closed')
            change = False
            break
        try:
            info = dataSocket2.recv(2048).decode()
        except:
            print("change tcp port")
            break
        print(info)
        print(dataPort)
        labels[id]["text"] = '-----------------------------\n'
        labels[id]["text"] += 'Client ' + \
            str(id) + '\nName: ' + str(clientName)+ '\nIP: ' + str(clientIP) +'\nServer DataPort: ' + \
                str(dataPort) + '\nDate: ' + str(registerTime[0]) +'\nRegister Time: ' + str(registerTime[1])  +'\n\n'
        labels[id]["text"] += '-----------------------------\n'

        if (info != ''):
           
            labels[id]["text"] += info.split()[0] + '\n'
            
            #CPU Temperature
            labels[id]["text"] += 'CPU: ' + info.split()[2] + info.split()[3] + '\n\n'
            
            #DISK
            labels[id]["text"] += 'DISK ' + '\n'
            labels[id]["text"] += 'Total: ' + info.split()[6] + ' Gb'+'\n'
            labels[id]["text"] += 'Used: ' + info.split()[8] +' Gb'+ '\n'
            labels[id]["text"] += 'Available: ' + info.split()[10] +' Gb'+ '\n'
            labels[id]["text"] += 'Used Persent: ' + info.split()[12] + '%'+ '\n \n'
            
            #memory
            labels[id]["text"] += 'MEMORY ' + '\n'
            labels[id]["text"] += 'Total: ' + info.split()[15] +' Gb'+ '\n'
            labels[id]["text"] += 'Used: ' + info.split()[17] +' Gb'+ '\n'
            labels[id]["text"] += 'Available: ' + info.split()[19] +' Gb'+ '\n'
            labels[id]["text"] += 'Used Persent: ' + info.split()[21] + '%'+ '\n'


            
            labels[id]["text"] += '-----------------------------\n'

            cpus[id]['value'] = info.split()[2]
            mems[id]['value'] = info.split()[21]
            disks[id]['value'] = info.split()[12]

            cpuLabels[id]['text'] = 'CPU temperature: ' + info.split()[2] + '\N{Degree Celsius}'
            memLabels[id]['text'] = 'Memory percentage: ' + info.split()[21] + '%'     
            diskLabels[id]['text'] = 'Disk percentage: ' + info.split()[12] + '%'


# def dataConnection(dataPort, id):
#     dataSocket = socket(AF_INET, SOCK_STREAM)
#     dataSocket.bind(('', dataPort))
#     dataSocket.listen(40)
#     while True:
#         # registerSocket.send('STATUS open\n'.encode())
#         dataSocket2, addr = dataSocket.accept()
#         dataConnection2Thread = Thread(
#             target=dataConnection2, args=(dataSocket2, dataPort, id, ))
#         dataConnection2Thread.start()
#         dataConnection2Threads.append(dataConnection2Thread)


def registerConnection(registerSocket, id):
    global change
    try:
        message = registerSocket.recv(
            2048).decode()
        
    except:
        registerSocket.close()
    #check register packet
    #if ... else
    #
    
    #check missing REGISTER
    if (message.split()[0] == ''):
        returnMessage = '100 Missing Header'
        registerSocket.send(returnMessage.encode())
    #check missing name
    elif (message.split()[2] == ''):
        returnMessage = '101 Missing Name'
        registerSocket.send(returnMessage.encode())
    #check missing ip
    elif (message.split()[4] == ''):
        returnMessage = '102 Missing IP'
        registerSocket.send(returnMessage.encode())
    #missing udp port
    elif (message.split()[6] == ''):
        returnMessage = '103 Missing UDP Port'
        registerSocket.send(returnMessage.encode())
    #missing time
    elif (message.split()[8] == ''):
        returnMessage = '104 Missing Time'
        registerSocket.send(returnMessage.encode())

    #wrong header
    elif (message.split()[0] != 'REGISTER'):
        returnMessage = '105 Wrong Header'
        registerSocket.send(returnMessage.encode())
    
    elif (message.split()[2].isnumeric()):
        returnMessage = '108 Wrong Name'
        registerSocket.send(returnMessage.encode())
    elif (checkIp(message.split()[4]) == False):
        returnMessage = '107 Invalid IP'
        registerSocket.send(returnMessage.encode())
    elif (int(message.split()[6]) <= 0 or int(message.split()[6]) > 65000):
        returnMessage = '106 Invalid Port'
        registerSocket.send(returnMessage.encode())

    else:
        # has no error.
        print(message)
        udpPort = int(message.split()[6])
        clientIP = message.split()[4]
        clientName = message.split()[2]
        registerTime = [message.split()[8] ,message.split()[9]]
        dataPort = serverPort + 1 + id
        returnMessage = 'REGISTER-REPLY\nSTATUS success\nID ' + \
            str(id) + '\nINTERVAL 5\nTCP_PORT ' + \
            str(dataPort) + '\n'
        registerSocket.send(returnMessage.encode())

        try:
            
            message2 = registerSocket.recv(
                2048).decode()
        except:
            registerSocket.close()
        #check message from client.
            #check protocol, check accpet
        
        if (message2.split()[0].isnumeric()):
            messagebox.showerror("Register Accept Fail",message2)
        #check missing
            #missing header
            
        elif (message2.split()[0] == ''):
            datasocketStatusMessage = '300 Missing Header'
            registerSocket.send(datasocketStatusMessage.encode())
        elif (message2.split()[2] == ''):
            datasocketStatusMessage = '301 Missing Status'
            registerSocket.send(datasocketStatusMessage.encode())
        
        elif (message2.split()[0] != 'DATAPORT'):
            datasocketStatusMessage = '302 Wrong Header'
            registerSocket.send(datasocketStatusMessage.encode())
        elif (message2.split()[2] != 'accept' and message2.split()[2] != 'deny'):
            datasocketStatusMessage = '303 Wrong Status'
            registerSocket.send(datasocketStatusMessage.encode())

    
        print(message2)
        result = message2.split()[2]
        if (result == 'accept'):
            # dataConnectionThread = Thread(
            #     target=dataConnection, args=(dataPort, id, ))
            # dataConnectionThread.start()
            # dataConnectionThreads.append(dataConnectionThread)
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.bind(('', dataPort))
            dataSocket.listen(40)
            registerSocket.send('DATAPORT-REPLY\nSTATUS open\n'.encode())
            
            
            dataSocket2, addr = dataSocket.accept()

            # check protocol recieve packet (SEND-ERROR)
                #if fail - close
            #if true
            
            # dataConnection2Thread = Thread(
            #     target=dataConnection2, args=(dataSocket2, dataPort, id, ))
            # dataConnection2Thread.start()
            # dataConnection2Threads.append(dataConnection2Thread)
            
            newLabel = tk.Label(text='Client ' + str(id) +
                                '\nDataPort ' + str(dataPort) + '\n')
            labels.append(newLabel)
            newLabel.grid(row=0, column=id)


            # changeTcpPortInput = tk.Entry(width=10)
            # changeTcpPortInputs.append(changeTcpPortInput)
            # changeTcpPortInput.grid(row=1, column=id)

            # #label for new interval
            # newLabelInterval = tk.Label(text='Interval')
            # labelsNewIntervals.append(newLabelInterval)
            # newLabelInterval.grid(row=3, column=id, sticky = 'w')
            # #--------------------------------------------
            
            # #Textbox for input new Interval
            # changeIntervalInput = tk.Entry(width=10)
            # changeIntervalInputs.append(changeIntervalInput)
            # changeIntervalInput.grid(row=4, column=id, sticky='w')
                    ### progress bar
            cpu = ttk.Progressbar(
                window,
                orient='horizontal',
                mode='determinate',
                length=280,
            )
            
            # place the progressbar
            cpu.grid(column=id, row=1)
            
            cpu_label = tk.Label(text=f"CPU temperature: {cpu['value']}\N{Degree Celsius}")
            cpu_label.grid(column=id, row=2)
            
            mem = ttk.Progressbar(
                window,
                orient='horizontal',
                mode='determinate',
                length=280,
            )
            mem.grid(column=id, row=3)
            
            mem_label = tk.Label(text=f"Memory percentage: {mem['value']}%")
            mem_label.grid(column=id, row=4)

            disk = ttk.Progressbar(
                window,
                orient='horizontal',
                mode='determinate',
                length=280,
            )
            disk.grid(column=id, row=5)
            
            disk_label = tk.Label(text=f"Disk percentage: {disk['value']}%")
            disk_label.grid(column=id, row=6)
        
            cpus.append(cpu)
            mems.append(mem)
            disks.append(disk)
            
            cpuLabels.append(cpu_label)
            memLabels.append(mem_label)
            diskLabels.append(disk_label)
            
            #label for new interval
            newLabelInterval = tk.Label(text='New Interval')
            labelsNewIntervals.append(newLabelInterval)
            newLabelInterval.grid(row=7, column=id, sticky = 'w')
            
            #Textbox for input new interval
            newInterval =tk.Entry(width=10)
            changeIntervalInputs.append(newInterval)
            newInterval.grid(row=7, column=id)
            
            
            #Button for changing Interval
            changIntervalButton = tk.Button(text='Change', command=partial(sendInterval, udpPort, clientIP, id))
            changIntervalButtons.append(changIntervalButton)
            changIntervalButton.grid(row=7, column=id, sticky='E')
            
            #label for new port
            newLabelPort = tk.Label(text='New Port')
            labelsNewPortInput.append(newLabelPort)
            newLabelPort.grid(row=8, column=id,sticky = 'w')
    
            #Textbox to for inputing new port        
            newPort =tk.Entry(width=10)
            changeTcpPortInputs.append(newPort)
            newPort.grid(row=8, column=id)

            #Button for changing Port
            changeTcpPortButton = tk.Button(text='Change', command=partial(changeTcpPort, udpPort, clientIP, id, clientName, registerTime))
            sendNewPortAndUdpButtons.append(changeTcpPortButton)
            changeTcpPortButton.grid(row=8, column=id, sticky='E')
            #-----------------------------------------
            
            window.columnconfigure(id, weight=1)

            # while True:
            #     if change == True:
            #         dataSocket2.close()
            #         dataSocket.close()
            #         change = False
            #         break
            #     try:
            #         info = dataSocket2.recv(2048).decode()
            #     except:
            #         print("change tcp port")
            #         dataSocket2.close()
            #         dataSocket.close()
            #         break

            #     print(info)
            #     labels[id]["text"] = '######################\n'
            #     labels[id]["text"] += 'client ' + \
            #         str(id) + '\ndataPort ' + str(dataPort) + '\n'
            #     labels[id]["text"] += info + '\n'
            #     labels[id]["text"] += '######################\n'

            newThread = Thread(target=dataConnection2, args=(
                dataSocket, dataSocket2, dataPort, id, clientName, clientIP, registerTime))
            newThread.start()
        elif (result == 'deny'):
            messagebox.showerror("Deny Accept","Conncetion Refused")

    
        # change tcp port for client
        # registerSocket.close()


def tcpConnection():
    id = 0
    serverSocket.listen(40)

    while True:
        print('Ready to register...')
       
        registerSocket, addr = serverSocket.accept()

        registerConnectionThread = Thread(target=registerConnection,
                                          args=(registerSocket, id, ))
        registerConnectionThread.start()
        registerConnectionThreads.append(registerConnectionThread)
        id+=1


# def udpConnection(newDataPort):
#     global udpPort
#     udpSocket = socket(AF_INET, SOCK_DGRAM)
#     control = 'TCP_PORT ' + str(newDataPort) + '\nINTERVAL 1\n'
#     udpSocket.sendto(control.encode(), ('localhost', udpPort))


tcpConnectionThreads = []
registerConnectionThreads = []
dataConnectionThreads = []
dataConnection2Threads = []


labels = []

labelsNewPortInput = []
changeTcpPortInputs = []
changeIntervalInputs = []
labelsNewIntervals = []
sendNewPortAndUdpButtons = []
udpPort = 0
clientInfos = []
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 3999
serverSocket.bind(('', serverPort))
changIntervalButtons = []

cpus= []
mems = []
disks = []

cpuLabels = []
memLabels = []
diskLabels = []

tcpConnectionThread = Thread(target=tcpConnection, args=())
tcpConnectionThread.start()
tcpConnectionThreads.append(tcpConnectionThread)


# for i in range(5):
#     print(i)
#     time.sleep(3)
# udpSocket = socket(AF_INET, SOCK_DGRAM)
# control = 'TCP_PORT 4000\nINTERVAL 1\n'
# udpSocket.sendto(control.encode(), ('localhost', 4001))
# print('send udp success 1')

# time.sleep(15)

# control = 'TCP_PORT 4000\nINTERVAL 5\n'
# udpSocket.sendto(control.encode(), ('localhost', 4001))
# print('send udp success 2')

window = tk.Tk()
window.title("Computer Resources Management")
window.rowconfigure(0, weight=1)
window.mainloop()

