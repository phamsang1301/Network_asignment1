from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import time
import tkinter as tk
from functools import partial
from tkinter import ttk
change = False

def changeTcpPort(udpPort, clientIP, id):
    global changeTcpPortInputs, change
    change = True

    newDataPort = int(changeTcpPortInputs[id].get())
    newInterval = int(changeIntervalInputs[id].get())
    print('abc ' + str(newDataPort))
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    control = 'CHANGE-DATAPORT\nNEW-DATAPORT ' + str(newDataPort) + '\nINTERVAL ' +str(newInterval)+'\n'
    # control = 'TCP_PORT ' + str(newDataPort) + '\nINTERVAL 1\n'    
    udpSocket.sendto(control.encode(), (clientIP, udpPort))
    # dataSocket2.close()
    
    #recieve protocol (SEND-ERROR-UDP)
        # if fail 
            # display error on clinet's screen
        # if true 
    newDataSocket = socket(AF_INET, SOCK_STREAM)
    newDataSocket.bind(('', newDataPort))
    newDataSocket.listen(40)
    # while True:
    #modify in client -- if status = open
    # registerSocket.send('STATUS open\n'.encode())
    newDataSocket2, addr = newDataSocket.accept()
    newThread = Thread(target=dataConnection2, args=(
        newDataSocket, newDataSocket2, newDataPort, id))
    newThread.start()


def dataConnection2(dataSocket, dataSocket2, dataPort, id):
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
    
    
    time.sleep(3)  # time to stop receiving info from previous dataPort
    global change
    while True:
        if change == True:
            # close socket
            dataSocket2.close()
            dataSocket.close()
            change = False
            break
        try:
            info = dataSocket2.recv(2048).decode()
        except:
            print("change tcp port")
            break
        print(info)
        labels[id]["text"] = '-----------------------------\n'
        labels[id]["text"] += 'Client ' + \
            str(id) + '\nDataPort ' + str(dataPort) + '\nIP: ' + str() +'\n'
        labels[id]["text"] += info + '\n'
        labels[id]["text"] += '-----------------------------\n'



        cpus[id]['value'] = info.split()[1]
        mems[id]['value'] = info.split()[20]
        disks[id]['value'] = info.split()[11]

        cpuLabels[id]['text'] = 'CPU temperature: ' + info.split()[1] + '\N{Degree Celsius}'
        memLabels[id]['text'] = 'Memory percentage: ' + info.split()[20] + '%'     
        diskLabels[id]['text'] = 'Disk percentage: ' + info.split()[11] + '%'


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
    print(message)
    udpPort = int(message.split()[6])
    clientIP = message.split()[4]
    
    dataPort = serverPort + 1 + id
    returnMessage = 'REGISTER-RETURN\nSTATUS success\nID ' + \
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
        dataSocket2, addr = dataSocket.accept()

        # registerSocket.send('DATASOCKET-STATUS\nSTATUS open\n'.encode())
        
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
        
        #Textbox to for input new interval
        newInterval =tk.Entry(width=10)
        changeIntervalInputs.append(newInterval)
        newInterval.grid(row=7, column=id)
        
        #label for new port
        newLabelPort = tk.Label(text='New Port')
        labelsNewPortInput.append(newLabelPort)
        newLabelPort.grid(row=8, column=id,sticky = 'w')
   
        #Textbox to for inputing new port        
        newPort =tk.Entry(width=10)
        changeTcpPortInputs.append(newPort)
        newPort.grid(row=8, column=id)
        
        #Button for changing Port and Interval
        changeTcpPortButton = tk.Button(width=10,
        text='Change', command=partial(changeTcpPort, udpPort, clientIP, id))
        sendNewPortAndUdpButtons.append(changeTcpPortButton)
        changeTcpPortButton.grid(row=9, column=id)
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
            dataSocket, dataSocket2, dataPort, id))
        newThread.start()
    else:
        # change tcp port for client
        registerSocket.close()


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

        id += 1


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
window.rowconfigure(0, weight=1)
window.mainloop()
