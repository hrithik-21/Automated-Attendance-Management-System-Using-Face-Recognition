from datetime import datetime
import os
import numpy
import cv2 as cv
import face_recognition as fg

list_img=os.listdir('img')
base_img=[]   #images
img_class=[]
base_encoding=[]

def encoding(base_img):
    img_encodings=[]
    for i in base_img:
        i=cv.cvtColor(i,cv.COLOR_BGR2RGB)
        encode_value=fg.face_encodings(i)[0]
        img_encodings.append(encode_value)
    return img_encodings

def attendance(markname):
    with open("att.csv","w+") as attend:
        data = attend.readlines()
        namelist = []
        for i in data:
            data1 = i.split(',')
            namelist.append(data1[0])
        if markname not in namelist:
            currtime=datetime.now()
            format_time= currtime.strftime("%H:%M:%S")
            attend.writelines(f'\n{name},{format_time}')

for i in list_img:
    #cur_img=cv.imread(f'{path}/{i}')
    cur_img = fg.load_image_file('img/'+str(i))
    base_img.append(cur_img)
    img_class.append(i.split(".")[0])
# print(base_img)
# print(img_class)
base_encoding=encoding(base_img)
#print(base_encoding)
capture=cv.VideoCapture(0)
while True:
    frame , cap = capture.read()
    simg = cv.resize(cap, (0,0), None, 0.25, 0.25)
    simg = cv.cvtColor(simg, cv.COLOR_BGR2RGB)
    faceinframe = fg.face_locations(simg)
    encodeframe = fg.face_encodings(simg, faceinframe)

    for floc, fencode in zip(faceinframe, encodeframe):
        match = fg.compare_faces(base_encoding, fencode)
        facedistance = fg.face_distance(base_encoding, fencode)

        print(facedistance)

        index= numpy.argmin(facedistance)
        if match[index]:
            y1, x2, y2, x1= floc
            y1, x2, y2, x1= y1*4, x2*4, 2*4, x1*4
            name= img_class[index].upper()
            print (name)
            cv.rectangle(cap, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv.putText(cap, name, (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
            attendance(name)
    cv.imshow("Image",cap)
    cv.waitKey(1)

print(len(base_encoding))
