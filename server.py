from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import time
import pickle
import tkinter as tk



def clientConnection(connectionSocket,id):
    global serverPort

    #Udp connection to sent new interval and port
    def udpConnection():
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        mess = {"port": newPort.get(), "interval": newInterval.get()}
        control = pickle.dumps(mess)
        udpSocket.sendto(control, ('localhost', UDP_Port))
        
    # new thread to open UDP connection
    def newUDPThread():
        newThread2 = Thread(target=udpConnection, args=())
        newThread2.start()
        #add UDP Thread into current client thread
        clients.append(newThread2)

    try:
        #Recive client's info
        message = connectionSocket.recv(
                2048)
        #turn message into object
        msg = pickle.loads(message)
        UDP_Port = msg['UDP_PORT']

        
        #Create overall labels for client
        newLabel = tk.Label(text='Client ' + str(id))
        labels.append(newLabel)
        newLabel.grid(row=0, column=id)
        
        #label for new interval
        newLabelInterval = tk.Label(text='Interval')
        labelsInterval.append(newLabelInterval)
        newLabelInterval.grid(row=1, column=id, sticky = 'w', pady = 2)
        
        #Textbox to for input new interval
        newInterval =tk.Entry(width=10)
        intervals.append(newInterval)
        newInterval.grid(row=1, column=id)
        
        #label for new interval
        newLabelPort = tk.Label(text='Port')
        labelsPort.append(newLabelPort)
        newLabelPort.grid(row=2, column=id,sticky = 'w', pady = 2 )
   
        #Textbox to for input new interval        
        newPort =tk.Entry(width=10)
        ports.append(newPort)
        newPort.grid(row=2, column=id)
        
        #Button to sent new interval and port
        newButton = tk.Button(text="Sent",  command=newThread)
        buttons.append(newButton)
        newButton.grid(row=3, column=id)
        
        
        window.columnconfigure(id, weight=1)
        
        
        #Return message to client (success or not) 
        #Note: Check error here, if error, sent error to client with Status = Failure
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
            labels[id]["text"] += 'Time: ' + str(msg['TIME']) + '\n \n'

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
 
# open tcp connection
def tcpConnection():
    global serverSocket, clients, labels, id
    serverSocket.listen(40)

    while True:
        print('Ready to server...')
        connectionSocket, addr = serverSocket.accept()

        #newwThread to open tcp connection
        
        newThread = Thread(target=clientConnection,
                           args=(connectionSocket, id, ))
        newThread.start()
        clients.append(newThread)
        id += 1        

            

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


window = tk.Tk()
window.rowconfigure(0, weight=1)
window.mainloop()


    