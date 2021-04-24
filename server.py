from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import time
import pickle
import tkinter as tk



def clientConnection(connectionSocket,id):
    global serverPort

    def udpConnection():
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        mess = {"port": 4000, "interval": 2}
        control = pickle.dumps(mess)
        # control = 'TCP_PORT 4000\nINTERVAL 2\n'
        udpSocket.sendto(control, ('localhost', UDP_Port))
    def newThread():
        newThread2 = Thread(target=udpConnection, args=())
        newThread2.start()
        clients.append(newThread2)

    try:
        #Recive client's info
        message = connectionSocket.recv(
                2048)
        #turn message into object
        msg = pickle.loads(message)
        UDP_Port = msg['UDP_PORT']

        
        #Create labels for client
        newLabel = tk.Label(text='Client ' + str(id))
        labels.append(newLabel)
        newLabel.grid(row=0, column=id)
        
        newLabelInterval = tk.Label(text='Interval')
        labelsInterval.append(newLabelInterval)
        newLabelInterval.grid(row=1, column=id, sticky = 'w', pady = 2)
        
        newInterval =tk.Entry(width=10)
        intervals.append(newInterval)
        newInterval.grid(row=1, column=id)
        
        
        newLabelPort = tk.Label(text='Port')
        labelsPort.append(newLabelPort)
        newLabelPort.grid(row=2, column=id,sticky = 'w', pady = 2 )
        
        newPort =tk.Entry(width=10)
        ports.append(newPort)
        newPort.grid(row=2, column=id)
        
        newButton = tk.Button(text="Sent",  command=newThread)

        buttons.append(newButton)
        newButton.grid(row=3, column=id)
        
        
        window.columnconfigure(id, weight=1)
        
        
        #Return message to client (success or not) 
        #Note: Check error here
        message_to_client = {'STATUS': "Success",'ID': id,'INTERVAL': 5, 'TCP_PORT': 4000 }
        msg_to_client = pickle.dumps(message_to_client)
        connectionSocket.send(msg_to_client)

        
        #recive and update client's computer info
        while True:
            info = connectionSocket.recv(
                2048)
            #turn info into object
            inf = pickle.loads(info)
            # display client  and client's computer info
            labels[id]["text"] = '----------------------\n'
            labels[id]["text"] += 'Client ' + str(id) + '\n \n'
            labels[id]["text"] += 'Name: ' + msg['NAME'] + ' \n'
            labels[id]["text"] += 'IP: ' + msg['IP'] + '\n '
            labels[id]["text"] += 'Port: ' + str(msg['UDP_PORT']) + '\n'
            labels[id]["text"] += 'Time: ' + str(msg['TIME']) + '\n '

            labels[id]["text"] += "CPU: "+ str(inf['CPU']) + " Degree" + '\n \n'
            labels[id]["text"] += "Memory: "  + '\n'
            labels[id]["text"] += "Total: " + str(inf['MEMORY']['Total']) + '\n'
            labels[id]["text"] += "Used: " + str(inf['MEMORY']['USED']) + '\n'
            labels[id]["text"] += "Available: " + str(inf['MEMORY']['Avaiable']) + '\n'
            labels[id]["text"] += "Use Percent: " + str(inf['MEMORY']['USED_PERCENT']) + '\n \n'
            labels[id]["text"] += "Disk: "  + '\n'
            labels[id]["text"] += "Total: " + str(inf['DISK']['Total']) + '\n'
            labels[id]["text"] += "Used: " + str(inf['DISK']['USED']) + '\n'
            labels[id]["text"] += "Available: " + str(inf['DISK']['Avaiable']) + '\n'
            labels[id]["text"] += "Use Percent: " + str(inf['DISK']['USED_PERCENT']) + '\n \n'
            labels[id]["text"] += '----------------------\n'
    except:
        connectionSocket.close()
 

def tcpConnection():
    global serverSocket, clients, labels, id
    serverSocket.listen(40)

    while True:
        print('Ready to server...')
        connectionSocket, addr = serverSocket.accept()

        newThread = Thread(target=clientConnection,
                           args=(connectionSocket, id, ))
        newThread.start()
        clients.append(newThread)
        id += 1        



def create_TCP_connection():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 4000
    serverSocket.bind(('', serverPort))
    serverSocket.listen(40)
    
    print('Ready to server...')

    while(True):
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(
                1024)
            msg = pickle.loads(message)
            
            print("Name: " +msg['NAME'])
            print("IP: " + msg['IP'])
            print("UDP PORT: " +str(msg['UDP_PORT']))
            print("Time: " +str(msg['TIME']))

            
            message_to_client = {'STATUS': "Success",'ID': id,'INTERVAL': 5, 'TCP_PORT': 4000 }
            msg_to_client = pickle.dumps(message_to_client)
            connectionSocket.send(msg_to_client)

            while True:
                info = connectionSocket.recv(
                    2048)
                inf = pickle.loads(info)
                # print(inf)
                print("CPU: "+ str(inf['CPU']) + " Degree")
                print("------------------------------")
                print("Memory: ")
                print("\t Total: " + str(inf['MEMORY']['Total']))
                print("\t Used: " + str(inf['MEMORY']['USED']))
                print("\t Available: " + str(inf['MEMORY']['Avaiable']))
                print("\t Use Percent: " + str(inf['MEMORY']['USED_PERCENT']))
                print("-------------------------------")      
                print("Disk: ")
                print("\t Total:" + str(inf['DISK']['Total']))
                print("\t USED: " + str(inf['DISK']['USED']))
                print("\t Available: " + str(inf['DISK']['Avaiable']))
                print("\t Use Percent: " + str(inf['DISK']['USED_PERCENT']))
                print("-------------------------------------------------------------")
                
                # send_new_para_to_client(1,4000)
        except:
            connectionSocket.close()
            
# def open_udp_connection():
#     udpSocket = socket(AF_INET, SOCK_DGRAM)
#     udpSocket.bind(('', 4001))


# def send_new_para_to_client(interval, tcp_port):
#     udpSocket = socket(AF_INET, SOCK_DGRAM)
#     socket.bind(('', 4000))
#     # socket.listen(40)
#     connectionSocket, addr = socket.accept()
#     if (True): 
#         # message_to_client = {'INTERVAL': interval, 'TCP_PORT': tcp_port }
#         # msg_to_client = pickle.dumps(message_to_client)
#         msgFromServer       = "Hello UDP Client"
#         bytesToSend         = str.encode(msgFromServer)
#         udpSocket.sendto(bytesToSend,('localhost', 4001) )


# def udpConnection():
#     udpSocket = socket(AF_INET, SOCK_DGRAM)
#     control = 'TCP_PORT 4000\nINTERVAL 2\n'
#     udpSocket.sendto(control.encode(), ('localhost', 4001))

threads = []
clients = []
labels = []
intervals = []
ports = []
buttons  = []
labelsInterval = []
labelsPort  =  []
id = 0
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 4000
serverSocket.bind(('', serverPort))

newThread = Thread(target=tcpConnection, args=())
newThread.start()
threads.append(newThread)

# newThread2 = Thread(target=udpConnection, args=())
# newThread2.start()
# clients.append(newThread2)


window = tk.Tk()
window.rowconfigure(0, weight=1)
window.mainloop()


    