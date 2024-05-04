import subprocess
import threading
from tkinter import *
from customtkinter import *
from communicate import Something
from test import num_processes
from multiprocessing import Process
from communicate import server_thread
import Pyro4
import time
from communicate import table
class Tab:
    def __init__(self, parent, name, num, tab_number,ps):
        self.ps=ps
        self.name = name
        self.num = num
        self.tab = parent.add(name)
        self.tab_number = tab_number
        self.combo=None
        self.message_box=None
        self.messages=None
        self.history=None
        self.create_widgets()
    #methode to create the interface
    def create_widgets(self):

        #creating a list for the names of each tab and to use it for the combo box
        name = [f"p{i + 1}" for i in range(self.num) if i != self.tab_number - 1]

        #creating the first row in the tab
        local_btn = CTkButton(self.tab, text="Local Event", command=self.trigger_local_event)
        local_btn.grid(row=0, column=0, padx=(10, 40), pady=10)
        send_btn = CTkButton(self.tab, text="Send", width=80, command=self.trigger_send_event)
        send_btn.grid(row=0, column=2, padx=10, pady=10)
        label2 = CTkLabel(self.tab, text="Received messages")
        label2.grid(row=0, column=3, padx=10, pady=10)

        #the second row
        self.messages = CTkTextbox(self.tab, height=60,state='disabled')
        self.messages.grid(row=1, column=3, padx=10, pady=10)

        #the third one
        label3 = CTkLabel(self.tab, text="Message")
        label3.grid(row=2, column=0, padx=10, pady=10)
        self.message_box = CTkEntry(self.tab)
        self.message_box.grid(row=2, column=1, padx=10, pady=10)
        self.combo = CTkComboBox(self.tab, values=name)
        self.combo.grid(row=2, column=2, padx=10, pady=10)

        #the forth row
        label4 = CTkLabel(self.tab, text="Vector Clock")
        label4.grid(row=3, column=1, padx=10, pady=10)

        #the fifth row
        label5 = CTkLabel(self.tab, text=f"History of p{self.tab_number}")
        label5.grid(row=3, column=3, padx=10, pady=10)

        #the last row
        self.history = CTkTextbox(self.tab, height=60,state='disabled')
        self.history.grid(row=4, column=3, padx=10, pady=10)


    #a methode that triggers the local event when pressed
    def trigger_local_event(self):
        #calling the methode from
        self.ps.local_event()
        print(self.tab_number)
        tab=tabs[self.tab_number-1]
        tab.history.configure(state='normal')
        tab.history.insert('end',f"Local: {table}\n")
        tab.history.configure(state='disabled')

    #a methode that triggers the send event
    def trigger_send_event(self):
        receiver_pid = int(self.combo.get()[1:]) - 1
        message = self.message_box.get()
        self.ps.send_event(receiver_pid, message)
        sender_tab=tabs[self.tab_number-1]
        receiver_tab = tabs[receiver_pid]
        print(f"{receiver_pid+1} received the message and this is what i got:{message}")

        receiver_tab.messages.configure(state='normal')
        receiver_tab.messages.insert('end', f"p{self.ps.pid+1}: {message}\n")
        receiver_tab.messages.configure(state='disabled')

        sender_table = table.copy()
        sender_table[receiver_pid] -= 1
        # print(f"og table:{table}, fake one: {sender_table}")
        # print(sender_table)
        sender_tab.history.configure(state='normal')
        sender_tab.history.insert('end', f"Send({self.tab_number}): {sender_table}\n")
        sender_tab.history.configure(state='disabled')

        receiver_tab.history.configure(state='normal')
        receiver_tab.history.insert('end', f"Rec({self.tab_number}): {table}\n")
        receiver_tab.history.configure(state='disabled')



    # def trigger_local_event(self):
    #     something_instance = Something(self.tab_number - 1, num_processes)
    #     something_instance.local_event()
    # def trigger_send_event(self):
    #     something_instance=Something(self.tab_number - 1, num_processes)
    #     something_instance.send_event(int(self.combo.get()[1:]), self.message_box.get())

window = CTk()
window.geometry('800x500')
set_appearance_mode('light')
set_default_color_theme('green')

def start_server(num):
    start_nameserver_path = r"E:\Pyro4-exemples\Pyro4-exemples\pyrohw\start_nameserver.py"
    subprocess.Popen(["python", start_nameserver_path, str(num)])
    base_port = 9090
    for i in range(num):
        port = base_port + i
        ps = Something(i, num)
        # Start the server thread for each process
        t = threading.Thread(target=server_thread, args=(ps, "localhost", port))
        t.daemon = True  # Set the thread as daemon so it will exit when the main program exits
        t.start()
    print("Pyro4 server started.")

def submit():
    num = int(num_processes_entry.get())
    start_nameserver_path = r"E:\Pyro4-exemples\Pyro4-exemples\pyrohw\start_nameserver.py"
    subprocess.Popen(["python", start_nameserver_path, str(num)])
    global tabs
    tabs = []
    base_port = 9090
    processes = []
    for i in range(num):
        port = base_port + i
        ps = Something(i, num)
        tab = Tab(bottom_part, f"   p{i+1}   ", num, i+1, ps)
        tabs.append(tab)
        print(f"Created Tab: {tab.name}, Process ID: {ps.pid}")
        p = Process(target=server_thread, args=(ps, "localhost", port))
        p.start()
        processes.append(p)

def call(self):
    self.Something.local_event()
top_part = CTkFrame(window)
top_part.configure(height=100, width=800)
top_part.pack()
top_part.pack_propagate(False)

label1 = CTkLabel(top_part, text="Provide the number of processes ")
label1.pack(side="left", pady=10, padx=(20, 0))

num_processes_entry = CTkEntry(top_part, width=50)
num_processes_entry.pack(side="left", padx=10, pady=10)

start_btn = CTkButton(top_part, text='Start', width=10, command=submit)
start_btn.pack(side="left", pady=10, padx=50)

exit_btn = CTkButton(top_part, text='Exit', width=10)
exit_btn.pack(side="left", pady=10)

bottom_part = CTkTabview(window)
bottom_part.configure(width=800, height=400)
bottom_part.pack(side="bottom")

window.mainloop()