import mysql.connector
from datetime import datetime
import random
from prettytable import PrettyTable as p
amt=0
db = mysql.connector.connect(host='localhost', user='root', password='root')
cur = db.cursor()
cur.execute("create database if not exists bank")
cur.execute("use bank")
cur.execute(
    "Create table if not exists customer (Name varchar(200),Phone_no bigint,Date_time datetime,Account_no bigint,amount int(10))")
cur.execute(
    "Create table if not exists logs (SR_NO int(200) Primary Key Auto_Increment,Account_no bigint,Operation enum('Deposit','Withdraw'),Amount int(200),Date_time datetime)"
)
print("\n:::::::::::::::::::WELCOME TO BANK:::::::::::::::::::::")
while True:
  print(
      '''1 for=> Account Creation      \n2 for=>Doing Transactions   \n3 for=> Exit '''
      )
  try:
    option = int(input("Enter Option[1/2/3]=>"))
  except ValueError:
    print("\n**********************************************")
    print("Invalid input. Please enter a valid integer.")
    print("**********************************************\n\n")
    continue
  if (option == 1):
    print("#----------[1]ACCOUNT CREATION----------#\n")
    n = input("[1]Enter the Name=>")
    ph = int(input("[2]Enter Phone_Number=>"))
    today1 = datetime.today()
    cur.execute("SELECT max(account_no) FROM customer")
    x = 1000000000
    records = cur.fetchall()
    if (records[0][0] != None):
      #print(records)
      x = records[0][0] + 1
    s = 'INSERT INTO customer values(%s,%s,%s,%s,%s)'
    t = (n, ph, today1, x, amt)
    cur.execute(s, t)
    db.commit()
    print("|-----------------------------------------------------|")
    print("| Congratulations! Account created successfully.... |")
    print("|-----------------------------------------------------|\n")
    print("|------YOUR ACCOUNT_NO[", x, "]----------|\n")
  elif (option == 2):
    print("#-------[2]DOING TRANSACTION----------#\n")
    h = int(input("Enter Account_no=>"))
    cur.execute("SELECT account_no FROM customer where Account_no=" + str(h))
    records = cur.fetchall()
    for i in records:
      if h == i[0]:
        flag = True
        print("------------------------------------------------------")
        print("*********YOUR Account_NO. is Correct*************")
        print("------------------------------------------------------")
        while (True):
          trans = input("Do you want to do any transaction?(y/n):")
          if (trans.lower() == "y"):
            print('''\n********Menu********
                        \n->1 for=> Deposit
                        \n->2 for=> Withdraw
                        \n->3 for=> Account Details
                        \n->4 for=> Printing receipt
                        \n->5 for=> Mini Statment
                        \n->6 for=> Exits
                        ''')
            try:
              ch = int(input("Enter 1,2,3,4,5 or 6=>"))
            except ValueError:
              print("\n**********************************************")
              print("Invalid input. Please enter a valid integer.")
              print("**********************************************\n\n")
              continue
            if (ch == 1):
              cur.execute("Select amount from customer where Account_no=" +str(h))
              row1 = cur.fetchone()
              print("Available balance is : ",row1[0])
              amt_deposit= int(input("Enter the Amount to be Deposit=>"))
              amt = row1[0] + amt_deposit
              cur.execute("UPDATE customer SET amount = " + str(amt) +" where Account_no=" + str(h))
              db.commit()
              cur.execute("insert into logs(Account_no,Operation,Amount,Date_time) value("+str(h)+",'Deposit',"+str(amt_deposit)+",date(now()))")
              db.commit()
              print("*--------------------------------*")
              print("*---New Current Balance=",amt, "---*")
              print("*--------------------------------*")
            elif (ch == 2):
              cur.execute("Select amount from customer where Account_no=" +str(h))
              row1 = cur.fetchone()
              print("Available balance is : ", row1[0])
              rs = int(input("Enter The Amount To Be Withdraw=>"))
              if (row1[0] < rs):
                print("*-------------------------------------*\n")
                print("******** Insufficient fund! ***********")
                print("Your balance is ", row1[0], "only.")
                print("Try with lesser amount than balance.")
                print("*-------------------------------------*\n")
              else:
                print("Available balance is : ", row1[0])
                m = row1[0] - rs
                cur.execute("UPDATE customer SET amount = " + str(m) +" where Account_no=" + str(h))
                db.commit()
                print("*-----------------------------------*")
                print("*----- Current Balance=", m, "---*")
                print("*-----------------------------------*")
                cur.execute("insert into logs(Account_no,Operation,Amount,Date_time) value("+str(h)+",'Withdraw',"+str(rs)+",date(now()))")
                db.commit()
            elif (ch == 3):
              cur.execute("Select * from customer where Account_no=" + str(h))
              row = cur.fetchone()
              print("*-------------ACCOUNT DETAILS---------*\n")
              print("Account Holder Name->", row[0])
              print("Phone_number=>", row[1])
              print("Account Number->", row[3])
              print("Account Balance->", row[4])
              print("*-----------------------------------*\n")
            elif (ch == 4):
              today = datetime.today()
              cur.execute("Select * from customer where Account_no=" + str(h))
              row = cur.fetchone()
              print("\n          Printing receipt.......")
              print("*************************************")
              print("                  BANK              ")
              print("*************************************")
              print("Timing:", today)
              print("*************************************")
              print("Account Holder Name->", row[0])
              print("Phone_number=>", row[1])
              print("Account Number->", row[3])
              print("Account Balance->", row[4], "\n")
              print("Thank You For Choosing Our Bank!")
              print("                  Visit Again!                  ")
              print("*************************************")
            elif (ch==5):
              cur.execute("SELECT * FROM logs where Account_no=" + str(h))
              rec =cur.fetchall()
              data=p(['SR_NO','Account_no','Operation','Amount','Date_time'])
              for i in rec:
                data.add_row(i)
              print(data)
            elif (ch == 6):
              print("""
                                ------------------------------------------
                                |    Thanks for choosing us as your bank |
                                |    Visit us again!                     |
                                ------------------------------------------
                                """)
              break    
            else:
              print("\n----------Invaild option-----------")
              print("Select option from(1,2,3,4 and 5)")
              print("-----------------------------------\n\n")
          elif (trans.lower() == "n"):
            print("""
                             ---------------------------------------
                             | Thanks for choosing us as your bank |
                             |          Visit us again!            |
                             ---------------------------------------
                             """)
            exit()
          else:
            print("\n************************************************")
            print("Wrong command!! Enter 'y' for YES and 'n' for no")
            print("************************************************\n\n")
  elif (option == 3):
    print("""
            ---------------------------------------
            | Thanks for choosing us as your bank |
            |           Visit us again!           |
            ---------------------------------------
            """)
    exit()
  else:
    print("\n----------Invaild option-----------")
    print("Select option from(1 ,2 & 3)")
    print("-----------------------------------\n\n")    
