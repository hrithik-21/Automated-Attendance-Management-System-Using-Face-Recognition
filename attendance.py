import addnewdept
import pandas as pd
import datetime
import os
import numpy
import cv2 as cv
import face_recognition as fg
import pymongo as pm

def attendance():

    myclient = pm.MongoClient("mongodb://localhost:27017/")
    mydept = myclient["Attendance"]
    collection = mydept["department"]
    print("Choose Branch Name(CS/IT/ECE)-:")
    print("1.Information Technology")
    print("2.Computer Science")
    print("3.Electronics and Communication Technology")
    choice = int(input(" Enter Your Choice-: "))
    if (choice == 1):
        dept = "it"
    elif (choice == 2):
        dept = "cs"
    elif (choice == 3):
        dept = "ece"
    sem = input("Enter Semester-:")
    dept=dept.upper()
    sem=sem.upper()
    if collection.count_documents({"Semester": sem, "Branch": dept}, limit=1) > 0:

        parentdir = "img"
        dir = dept + "-" + "Sem " + sem
        path = os.path.join(parentdir, dir)    # path of the image

        list_img = os.listdir(path)            # list of images in directory
        base_img = []                          # contain numpy array of images
        img_class = []                         # list of images without extension
        base_encoding = []

        today_date = datetime.datetime.now()
        date=datetime.date.today()
        today = date.strftime("%d/%m/%Y")
        month = today_date.month
        year = today_date.year
        filename = "Sem" + sem + "-" + dept + "-" + str(month) + "-" + str(year) + ".csv"
        filepath = os.path.join('files/', filename)
        df = pd.read_csv(filepath)
        if(df[today].isnull().values.any()):
            df[today] = "Absent"
            df.to_csv(filepath, index=False)


        def encoding(base_img):
            img_encodings = []
            for i in base_img:
                i = cv.cvtColor(i, cv.COLOR_BGR2RGB)
                encode_value = fg.face_encodings(i)[0]
                img_encodings.append(encode_value)
            return img_encodings               # return encoding(128 different values) of the images in the list

        def mark_attendance(rollno):
            filename = "Sem"+sem+"-"+ dept + "-" + str(month) + "-" + str(year) + ".csv"
            filepath = os.path.join('files/', filename)
            #print(filepath)
            df = pd.read_csv(filepath)
            rolls=[rollno]
            df.loc[df['RollNo'].isin(rolls), today] = 'Present'

            df.to_csv(filepath,index=False)

        name_class=[]
        for i in list_img:
            cur_img=cv.imread(f'{path}/{i}')
            #cur_img = fg.load_image_file(path + str(i))
            base_img.append(cur_img)
            img_class.append(i.split(".")[0])
            name_class.append(i.split(".")[1])

        base_encoding = encoding(base_img)     # contains the list of encodings of all the images
        capture = cv.VideoCapture(0)

        while True:

            frame, cap = capture.read()
            simg = cv.resize(cap, (0, 0), None, 0.25, 0.25)
            simg = cv.cvtColor(simg, cv.COLOR_BGR2RGB)
            faceinframe = fg.face_locations(simg)
            encodeframe = fg.face_encodings(simg, faceinframe)

            for floc, fencode in zip(faceinframe, encodeframe):
                match = fg.compare_faces(base_encoding, fencode)
                facedistance = fg.face_distance(base_encoding, fencode)

                index = numpy.argmin(facedistance)

                if (match[index] and facedistance[index] < 0.5):
                    y1, x2, y2, x1 = floc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    name = name_class[index]
                    rol = img_class[index]
                    print(name)
                    cv.rectangle(cap, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv.putText(cap, name, (x1, y1-2), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
                    mark_attendance(rol)

            cv.imshow("Image", cap)
            cv.waitKey(1)

    else:
        print("Sorry!!! Your Entered details Are Not Found In our Database")
        print("\nDo you want to add this department and branch in databse??(y or n)")
        ch=input()
        if ch=='y':
            addnewdept.addnewdept()
