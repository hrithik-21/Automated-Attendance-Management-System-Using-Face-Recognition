import pymongo as pm
import csv
import datetime
import calendar
import os

def addnewdept():

    myclient = pm.MongoClient("mongodb://localhost:27017/")
    mydept=myclient["Attendance"]
    collection=mydept["department"]
    #collection.drop()
    print("Choose Branch Name(CS/IT/ECE)-:")
    print("1.Information Technology")
    print("2.Computer Science")
    print("3.Electronics and Communication Technology")
    choice=int(input(" Enter Your Choice-: "))

    if(choice==1):
        dept="it"
    elif(choice==2):
        dept="cs"
    elif(choice==3):
        dept="ece"
    sem =input("Enter Semester-:")
    dept =dept.upper()
    sem =sem.upper()

    # cursor = collection.find({"Semester" : sem , "Branch" : dept })
    # for document in cursor:
    #     print(document)

    data = {"Semester": sem, "Branch": dept}
    if collection.count_documents({"Semester" : sem , "Branch" : dept }, limit = 1) > 0:
        print(f'{dept} Branch {sem} is already present')
        print(f"Do you want to reinsert this semester {sem} of {dept} department")
        choice =input("Yes Or No?(y/n)")
        if(choice=='y'):
            stu = int(input("Enter Maximum No'Of Students To Be Enrolled-:"))
            data["Students"] = stu
            parentdir="img"
            dir=dept+"-"+"Sem "+sem
            path = os.path.join(parentdir, dir)
            if os.path.isdir(path):
                print(f"Directory of {dept} department semester {sem} is already present -:")
                ch=input("Do You Want To Recreate?(y/n)")
                if(ch=='y'):
                    os.rmdir(path)
                    os.mkdir(path)
            else:
                os.mkdir(path)

            print(f"Now insert student images in {path}")
            ch=input(f"Press y if image is inserted in {path}-:")
            if(ch=='y'):
                base_img=[]
                list_img = os.listdir(path)
                for i in list_img:
                    base_img.append(i.split(".")[1])

                today_date = datetime.datetime.now()
                month = today_date.month
                year = today_date.year
                filename = "Sem"+sem+"-"+ dept + "-" + str(month) + "-" + str(year) + ".csv"
                filepath = os.path.join('files/', filename)
                with open(filepath, "w", newline='') as file:
                    csvwriter = csv.writer(file)
                    num_days = calendar.monthrange(year, month)[1]  # return no of days in a month
                    days = [datetime.date(year, month, day).strftime("%d/%m/%Y") for day in
                            range(1, num_days + 1)]  # return the list of dates in that month
                    fields = ['RollNo', 'Name']
                    fields.extend(days)  # it append the values present in the list days to fields
                    #fields.append("Percentage")
                    csvwriter.writerow(fields, )
                    l = []
                    for i,j in zip(range(1, stu + 1), base_img):  # writes roll no in csv file
                        file_data = [i,j]
                        csvwriter.writerow(file_data)
                collection.insert_one(data)  # insert data in database

                print("Inserted Successfully In Our Database")

        else:
            print("Insertion Aborted")
    else:
        stu = int(input("Enter Maximum Strength To Be Enrolled-:"))

        data["Students"] = stu
        parentdir = "img"
        dir = dept + "-" + "Sem " + sem
        path = os.path.join(parentdir, dir)
        os.mkdir(path)

        print(f"Now insert student images in {path}")
        ch = input(f"Press y if image is inserted in {path}-:")
        if (ch == 'y'):
            base_img = []
            list_img = os.listdir(path)
            for i in list_img:
                base_img.append(i.split(".")[1])

            today_date = datetime.datetime.now()
            month = today_date.month
            year = today_date.year
            filename = "Sem"+sem+"-"+ dept + "-" + str(month) + "-" + str(year) + ".csv"
            filepath = os.path.join('files/', filename)
            with open(filepath, "w", newline='') as file:
                csvwriter = csv.writer(file)
                num_days = calendar.monthrange(year, month)[1]  # return no of days in a month
                days = [datetime.date(year, month, day).strftime("%d/%m/%Y") for day in
                        range(1, num_days + 1)]  # return the list of dates in that month

                fields = ['RollNo', 'Name']
                fields.extend(days)  # it append the values present in the days list to fields
                #fields.append("Percentage")
                csvwriter.writerow(fields, )

                for i, j in zip(range(1, stu + 1), base_img):  # writes roll no in csv file
                    file_data = [i, j]
                    csvwriter.writerow(file_data)

            collection.insert_one(data)  # insert data in database
            print("Data Inserted Succesfully In our Database")

        #print('does not exist')
    return
# addnewdept()



    