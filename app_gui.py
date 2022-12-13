
import socket
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from PIL import ImageTk,Image

from pathlib import Path
import threading
import json
import pandas as pd

HOST = 'localhost'
PORT = 6969
HEADER = 64
FORMAT = "utf8"
DISCONNECT = "x"

LARGE_FONT = ("verdana", 13,"bold")


img_dir = "images_client/"
buffer_size = 1024

def write_img (s, file_name, buffer_size):
    #kiem tra xem thu muc co ton tai hay khong
    Path(img_dir).mkdir(parents=True, exist_ok=True)
    
    img = open(img_dir + file_name,'wb')
    data, addr = s.recvfrom(buffer_size)
    while (data!=b'Done'):
        img.write(data)
        data, addr = s.recvfrom(buffer_size)
    img.close()

def get_thumbnail (idx, destination, buffer_size):
    #Gui tin hieu toi server, nhan lai ten file
    client.sendto(('thumbnail'+str(idx)).encode(), (HOST, PORT))
    data,addr = client.recvfrom(buffer_size)

    write_img (client, data.decode(), buffer_size)
    return 1

def get_all_img (idx, destination, buffer_size):
    count = 0
    #Gui tin hieu toi server, nhan lai ten file
    client.sendto(('allimg'+str(idx)).encode(), (HOST, PORT))
    data,addr = client.recvfrom(buffer_size)
    while (data!=b'Done'):
        count+=1
        write_img (client, data.decode(), buffer_size)        
        data,addr = client.recvfrom(buffer_size)
    return count







#ứng dụng 
class TouristArear_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #kích thước cửa sổ ứng dụng
        self.geometry("500x200")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)
        self.title("famous tourist area")

        #frame cha chứa tất cả các frame con
        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        frame = HomePage(container, self)
        self.frames[HomePage] = frame 

        frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(HomePage)
        
    #hiển thị frame
    def showFrame(self, container):
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("700x500")
        frame.tkraise()

    # box hiển thị khi bạn đóng chương trình
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            return

#trang chính của ứng dụng
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")

        #nút để hiện thông tin cấc địa điểm có trong server
        label_title = tk.Label(self, text="HOME PAGE", font=LARGE_FONT,fg='#20639b',bg="bisque2")
        button_list = tk.Button(self, text="List all", bg="#20639b",fg='#f5ea54',command=self.listAll)

        #tìm kiếm địa chỉ dựa vào ID
        self.entry_search = tk.Entry(self)
        button_search = tk.Button(self, text="Search for ID",bg="#20639b",fg='#f5ea54', command=self.searchDetail)

        label_title.pack(pady=10)

        button_search.configure(width=10)
        button_list.configure(width=10)
        

        self.entry_search.pack()

        #nhãn để hiển thị lỗi khi xuất hiện lỗi
        self.label_notice = tk.Label(self, text="", bg="bisque2" )
        self.label_notice.pack(pady=4)

        button_search.pack(pady=2)
        button_list.pack(pady=2) 
        
        #frame xuất các dữ liệu chi tiết của một địa điểm
        self.frame_detail = tk.Frame(self, bg="steelblue1")
        
        self.label_name = tk.Label(self.frame_detail,bg="steelblue1", text="", font=LARGE_FONT)
        self.label_laditude_longditude = tk.Label(self.frame_detail,bg="steelblue1", text="", font=LARGE_FONT)
        self.label_description = tk.Label(self.frame_detail,bg="steelblue1", text="", font=LARGE_FONT)
        #nút bấm để show các ảnh cho địa điểm cụ thể
        self.button_allimg = tk.Button(self.frame_detail,text="show image",bg="#20639b",fg='#f5ea54')
        

        self.label_name.pack(pady=5)
        self.label_laditude_longditude.pack(pady=5)
        self.label_description.pack(pady=5)
        self.button_allimg.pack(pady=10)
        

        #frame xuất các dữ liệu về cấc địa điểm trong server
        self.frame_list = tk.Frame(self, bg="tomato")
        
        self.tree = ttk.Treeview(self.frame_list)

        self.tree["column"] = ("ID", "name")
        
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor='c', width=30)
        self.tree.column("name", anchor='e', width=140)


        self.tree.heading("0", text="", anchor='c')
        self.tree.heading("ID", text="ID", anchor='c')
        self.tree.heading("name", text="name", anchor='e')

        self.tree.pack(pady=20)

    #method lấy tát cả dữ liệu từ server (câu 1)
    def listAll(self):
        try:
            self.frame_detail.pack_forget()
            option = b'list'
            client.sendto(option,(HOST,PORT))

            x =self.tree.get_children()
            for item in x:
                self.tree.delete(item)
            data,addr = client.recvfrom(1024)
            data = json.loads(data.decode())


            for index in data['idx']:
                self.tree.insert(parent="",index="end",iid=index - 1,values=(index,data["name"][index - 1]))
                
            self.frame_list.pack()
        except:
            self.label_notice["text"] = "Error"

    #method để tìm kiếm thông tin chi tiết cho một địa điểm (câu 2)
    def searchDetail(self):
        try:
            self.frame_list.pack_forget()
            if self.entry_search.get() == "":
                self.label_notice["text"] = "null"
                return
            idx = int(self.entry_search.get()) - 1
            option = 'detail' + str(idx)
            

            client.sendto(option.encode(),(HOST,PORT))
            data, addr = client.recvfrom(1024)
            data = json.loads(data.decode())

            self.label_name['text'] = data['name']
            self.label_laditude_longditude['text'] = '(' + str(data['laditude']) + ',' + str(data['longditude']) + ')'
            self.label_description['text'] = data['description']

            self.frame_detail.pack()
        except:
            self.label_notice["text"] = "error"
        


        
            


client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

app = TouristArear_App()
#main
try:
    app.mainloop()
except:
    print("Error: server is not responding")





