from addnewdept import addnewdept
from attendance import attendance
from prevattendance import prevattendance

actions = {                               # Dictionary Contains Functions Name
            1: addnewdept,
            2: attendance,
            3:prevattendance,
           # 4:exit_page
        }
def main():
    #os.system('cls')
    print()
    print("1.Add New Department")
    print("2.Take Attendance")
    print("3.See Previous Attendance")
    print("4.Exit")
    choice = int(input("Enter Your Choice-:"))
    try:
        actions[choice]()
        main()
    except KeyError:
        print("Wrong Choice")
        main()
if __name__ == "__main__":
    main()