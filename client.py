from socket import *
import json
import pandas as pd
from pathlib import Path

img_dir = "images_client/"
buffer_size = 1024
server_ip = 'localhost'
server_port = 6969

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
    s.sendto(('thumbnail'+str(idx)).encode(), (server_ip, server_port))
    data,addr = s.recvfrom(buffer_size)

    write_img (s, data.decode(), buffer_size)
    return 1

def get_all_img (idx, destination, buffer_size):
    count = 0
    #Gui tin hieu toi server, nhan lai ten file
    s.sendto(('allimg'+str(idx)).encode(), (server_ip, server_port))
    data,addr = s.recvfrom(buffer_size)
    while (data!=b'Done'):
        count+=1
        write_img (s, data.decode(), buffer_size)        
        data,addr = s.recvfrom(buffer_size)
    return count

#mo socket
s = socket(type=SOCK_DGRAM)

#CAU 1

#gui tin hieu list toi local host (thay bang ip server neu xai qua mang Lan)
s.sendto(b'list', (server_ip, server_port))

#nhan du lieu tu server
data,addr = s.recvfrom(1024)
print (pd.DataFrame(json.loads(data.decode())))

#CAU 2

s.sendto(b'detail2', (server_ip, server_port))

data,addr = s.recvfrom(1024)
print (pd.DataFrame(json.loads(data.decode()), index=[0]))

#CAU 4

get_thumbnail (1, (server_ip, server_port), buffer_size)

#CAU 5

get_all_img (1, (server_ip, server_port), buffer_size)
