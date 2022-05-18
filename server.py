import json
import glob
def createData ():
    data = {'idx':{}, 'name':{}, 'laditude':{}, 'longditude':{}, 'description':{}, 'profile_image':{}, 'images_dir':{}}
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

data = createData ()
writedata (data, 'result.json')

#from socket import *
#s = socket(type=SOCK_DGRAM)
#s.bind(('localhost',5000))

#while True:
#    data,addr = s.recvfrom(1024)
#    print(data,addr)
#    s.sendto(data,addr)
