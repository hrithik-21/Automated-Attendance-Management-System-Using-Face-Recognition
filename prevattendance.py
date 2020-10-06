import pandas as pd
import datetime
import os

def prevattendance():

    # myclient = pm.MongoClient("mongodb://localhost:27017/")
    # mydept = myclient["Attendance"]
    # collection = mydept["department"]
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
    dept = dept.upper()
    sem = sem.upper()
    today_date = datetime.datetime.now()
    month = today_date.month
    year = today_date.year
    filename = "Sem" + sem + "-" + dept + "-" + str(month) + "-" + str(year) + ".csv"
    filepath = os.path.join('files/', filename)
    if(os.path.isfile(filepath)):
        df=pd.read_csv(filepath)
        print("Enter date(dd\mm\yyyy)")
        d=input()
        Value_Target = df[["RollNo","Name",d]]
        
        print(Value_Target)
    else:
        print("Sorry This File Does Not Exist")