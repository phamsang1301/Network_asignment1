from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import time
import pickle
from tkinter import messagebox  
import tkinter as tk
from tkinter import ttk




def clientConnection(connectionSocket,id):
    global serverPort

    #Udp connection to sent new interval and port
    def udpConnection():
        udpSocket = socket(AF_INET, SOCK_DGRAM)
        mess = {"port": newPort.get(), "interval": newInterval.get()}
        control = pickle.dumps(mess)
        udpSocket.sendto(control, ('localhost', clientUdpPort))

    # new thread to open UDP connection
    def newUDPThread():
        if (newInterval.get() == '' and newPort.get() == ''):
            messagebox.showerror("Error","Para must not be empty!")
        elif  newInterval.get() != '' and int(newInterval.get()) <= 0: 
            messagebox.showerror("Error","Invalid value!")
        elif newPort.get() != '' and int(newPort.get()) <= 0:
            messagebox.showerror("Error","Invalid value!")
        else:
            messagebox.showinfo("Success", "Done!")
            newThread2 = Thread(target=udpConnection, args=())
            newThread2.start()
            #add UDP Thread into current client thread
            clients.append(newThread2)

    try:
        #Recive client's info
        message = connectionSocket.recv(
                2048).decode()

        #turn message into object
        # if 
        # msg = pickle.loads(message)
        
        
        clientUdpPort = int(message.split()[5])

        #Create overall labels for client
        newLabel = tk.Label(text='Client ' + str(id))
        labels.append(newLabel)
        newLabel.grid(row=0, column=id)
        
        
        
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
        newLabelInterval = tk.Label(text='Interval')
        labelsInterval.append(newLabelInterval)
        newLabelInterval.grid(row=7, column=id, sticky = 'w', pady = 2)
        
        #Textbox to for input new interval
        newInterval =tk.Entry(width=10)
        intervals.append(newInterval)
        newInterval.grid(row=7, column=id)
        
        #label for new interval
        newLabelPort = tk.Label(text='Port')
        labelsPort.append(newLabelPort)
        newLabelPort.grid(row=8, column=id,sticky = 'w', pady = 2 )
   
        #Textbox to for input new interval        
        newPort =tk.Entry(width=10)
        ports.append(newPort)
        newPort.grid(row=8, column=id)
        
        #Button to sent new interval and port
        newButton = tk.Button(text="Send",  command=newUDPThread)
        buttons.append(newButton)
        newButton.grid(row=9, column=id)
        
        
        
        window.columnconfigure(id, weight=1)
        
        
        #Return message to client (success or not) 
        #Note: Check error here, if error, sent error to client with Status = Failure
        returnMessage = 'STATUS Success\nID ' + str(id) + '\nINTERVAL 5\nTCP_PORT ' + str(serverPort) + '\n'
        connectionSocket.send(returnMessage.encode())        
        # msg_to_client = pickle.dumps(message_to_client)
        connectionSocket.send(returnMessage.encode())


        #recive and update client's computer info
        while True:
            info = connectionSocket.recv(
                2048)
            #turn info into object
            inf = pickle.loads(info)
            # # display client  and client's computer info
            labels[id]["text"] = '----------------------\n'
            labels[id]["text"] += 'Client ' + str(id) + '\n \n'
            # labels[id]["text"] += 'Name: ' + message.split()[2] + ' \n'
            # labels[id]["text"] += 'IP: ' + message.split()[4] + '\n '
            # labels[id]["text"] += 'Port: ' + message.split()[6] + '\n'
            # labels[id]["text"] += 'Time: ' + str(msg['TIME']) + '\n \n'
            
            labels[id]["text"] += message + "\n \n"
            labels[id]["text"] += "CPU: "+ str(inf['CPU']) + '\N{Degree Celsius}' + '\n \n'
            labels[id]["text"] += "Memory: "  + '\n'
            labels[id]["text"] += "Total: " + str(inf['MEMORY']['Total']) + '\n'
            labels[id]["text"] += "Used: " + str(inf['MEMORY']['USED']) + '\n'
            labels[id]["text"] += "Available: " + str(inf['MEMORY']['Avaiable']) + '\n'
            labels[id]["text"] += "Used Percent: " + str(inf['MEMORY']['USED_PERCENT']) + '\n \n'
            labels[id]["text"] += "Disk: "  + '\n'
            labels[id]["text"] += "Total: " + str(inf['DISK']['Total']) + '\n'
            labels[id]["text"] += "Used: " + str(inf['DISK']['USED']) + '\n'
            labels[id]["text"] += "Available: " + str(inf['DISK']['Avaiable']) + '\n'
            labels[id]["text"] += "Used Percent: " + str(inf['DISK']['USED_PERCENT']) + '\n \n'
            labels[id]["text"] += '----------------------\n'
            
            cpus[id]['value'] = inf['CPU']
            mems[id]['value'] = inf['MEMORY']['USED_PERCENT']
            disks[id]['value'] = inf['DISK']['USED_PERCENT']

            cpuLabels[id]['text'] = 'CPU temperature: ' + str(inf['CPU']) + '\N{Degree Celsius}'
            memLabels[id]['text'] = 'Memory percentage: ' + str(inf['MEMORY']['USED_PERCENT']) + '%'     
            diskLabels[id]['text'] = 'Disk percentage: ' + str(inf['DISK']['USED_PERCENT']) + '%'

            # # label
            # value_label = ttk.Label(text=f"Current Progress: {pb['value']}%")
            # value_label.grid(column=id, row=5, columnspan=2)

            # # start button
            # start_button = ttk.Button(
            #     window,
            #     text='Progress',
            #     command=progress
            # )
            # start_button.grid(column=id, row=6, padx=10, pady=10, sticky=tk.E)

            # stop_button = ttk.Button(
            #     window,
            #     text='Stop',
            #     command=stop
            # )
            # stop_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)      
            # def progress():
            #     if pb['value'] < 100:
            #         pb['value'] += 20
            #         value_label['text'] = f"Current Progress: {pb['value']}%"
            #     else:
            #         messagebox.showinfo(message='The progress completed!') 
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

cpus= []
mems = []
disks = []

cpuLabels = []
memLabels = []
diskLabels = []

id = 0
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 4000
serverSocket.bind(('', serverPort))

newThread = Thread(target=tcpConnection, args=())
newThread.start()
threads.append(newThread)


window = tk.Tk()
window.title("Client Management")
window.rowconfigure(0, weight=1)
window.mainloop()


