import json
import glob
import os, time
img_dir = "images/"
buffer_size = 512
json_dir = "result.json"
server_ip = '192.168.56.1'
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
    
def writeData (data, dir_to_file):
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
        time.sleep (0.0001)
    img.close()
    time.sleep (0.01)
    s.sendto(str('Done').encode(),addr)
    
def send_all_img (idx, s, addr, buffer_size):
    for file in glob.glob(img_dir+str(idx)+"_*"):
        send_image (file, s, addr, buffer_size)
    time.sleep (0.01)
    s.sendto(b'Done',addr)        
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
    data = data.decode()
    print ("Received ",data," from: ",addr)
    if (data.startswith('list')):
        data_string = json.dumps(getList(database))
        s.sendto(str.encode(data_string), addr)
        
    elif (data.startswith('detail')):
        data_string = json.dumps(getDetail(database, int (data[6:len(data)])))
        s.sendto(str.encode(data_string), addr)
        
    elif (data.startswith('thumbnail')):
        send_image(img_dir+data[9:len(data)] + ".jpg", s, addr, buffer_size)
        
    elif (data.startswith('allimg')):
        send_all_img (data[6:len(data)], s, addr, buffer_size)
        
    else:
        s.sendto(data,addr)
