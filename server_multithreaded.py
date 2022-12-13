import json
import glob
import os
import threading
img_dir = "images/"
buffer_size = 1024
json_dir = "result.json"
server_ip = 'localhost'
server_port = 6969

def createData ():
    data = {'idx':{}, 'name':{}, 'laditude':{}, 'longditude':{}, 'description':{}}
    data ['idx'] = 1,2,3
    data ['name'] = "Hang son doong", "Tiem net", "DH KHTN"
    data ['laditude'] = 12.69,24.69,35.69
    data ['longditude'] = 13.70,25.70,36.70
    data ['description'] = "Your mother", "Nhà thứ 2 của dân chuyên tin", "Học như chơi"
    return data

def getProfileImageDir(idx):
    image_list = glob.glob("images/"+str(idx)+".*")
    return len(image_list), image_list
    
def getImagesDir (idx):
    images = glob.glob("images/"+str(idx)+"_*")
    return len(images), images
    
def writedata (data, dir_to_file):
    with open(dir_to_file, 'w') as fp:
        json.dump(data, fp)

def readData (dir_to_file):
    with open(dir_to_file, 'r') as fp:
        data = json.load(fp)
    return data

#database = createData ()
#writeData (database, json_dir)
database = readData (json_dir)

def getList(dtb):
    return {k:v for k,v in dtb.items() if (k=='idx') or (k=='name')}
def getDetail (dtb, idx):
    return {k:v[idx] for k,v in dtb.items()}

def send_image(file_path, s, addr, buffer_size):
    img = open(file_path,'rb')
    s.sendto((os.path.split(file_path)[1]).encode(),addr)
    while True:
        data_string = img.readline(buffer_size)
        if not data_string:
            break
        s.sendto(data_string, addr)
    img.close()
    s.sendto(b'Done',addr)
    
def send_all_img (idx, s, addr, buffer_size):
    for file in glob.glob(img_dir+str(idx)+"_*"):
        send_image (file, s, addr, buffer_size)
    s.sendto(b'Done',addr)      
    
def Process(data, addr):
    data = data.decode()
    
    if (data.startswith('list')):
        data_string = json.dumps(getList(database))
        s.sendto(str.encode(data_string), addr)
        
    elif (data.startswith('detail')):
        data_string = json.dumps(getDetail(database, int (data[6:len(data)])))
        s.sendto(str.encode(data_string), addr)
        
    elif (data.startswith('thumbnail')):
        threading._start_new_thread(send_image,(img_dir+data[9:len(data)] + ".jpg", s, addr, buffer_size))
        
    elif (data.startswith('allimg')):
        threading._start_new_thread(send_all_img, (data[6:len(data)], s, addr, buffer_size))
        
    else:
        s.sendto(data,addr)
################################
#1) 'list'
#2) 'detail2'
#4) 'thumbnail2'
#5) 'allimg2'
#send(bytes(str(num), 'utf8'))
from socket import *
s = socket(type=SOCK_DGRAM)
s.bind((server_ip, server_port))

while True:
    data,addr = s.recvfrom(buffer_size)
    threading._start_new_thread(Process,(data,addr))
    #tmp = threading.Thread(target = Process, kwargs=(data,addr))
    #tmp.start()
    
