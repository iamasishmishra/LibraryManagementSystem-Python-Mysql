from sqlalchemy import create_engine



#all the modules


import matplotlib.pyplot as plt
import mysql.connector as sqlt
import pandas as pd
engine = create_engine("mysql+mysqlconnector://root:Asishk@123@localhost:3306/librarysystem")
from tabulate import tabulate

con = sqlt.connect(host = "localhost", user = "root", passwd = "Asishk@123", database = "librarysystem")
cursor = con.cursor()

#BOOK DETAILS METHOD 

def bookInput():
    try:
        bookId = input("Enter Book Id: ")
        bookName = input("Enter Book Name: ")
        authorName = input ("Enter Book Author Name: ")
        bookPrice = input("Enter Book price: ")
        copies = input("Enter No of copies: ")
        qry = "Insert into book values({},'{}','{}',{},{},{})".format(bookId,bookName,authorName,bookPrice,copies,copies)
        cursor.execute(qry)
        con.commit()
        print("Added Successfully....")

    except:
        print("Error... Wrong Entry")

def bookEdit():
       x= int(input("Enter Book Id: "))
       qry = "select * from book where bookId = {}".format(x)
       cursor.execute(qry)
       
       r = cursor.fetchone()
       if r:
              y = float(input("Enter New Price: "))
              qry = "update book set bookPrice = {} where bookId = {}".format(y,x)
              cursor.execute(qry)
              con.commit()
              print("Edited Successfully... ")
       else:
              print("Wrong book Id")


def bookDelete():
       x= int(input("Enter Book Id: "))
       qry = "select * from book where bookId = {}".format(x)
       cursor.execute(qry)
       r = cursor.fetchone()
       if r:
              qry = "delete from book where bookId = {}".format(x)
              cursor.execute(qry)
              con.commit()
              print("Deleted Successfully... ")
       else:
              print("Wrong book Id")

def bookSearch():
       x= int(input("Enter Book Id: "))
       qry = "select * from book where bookId = {}".format(x)
       cursor.execute(qry)
       r = cursor.fetchone()
       if r:
              
              df = pd.read_sql("SELECT * FROM book", engine)
              print(tabulate(df, tablefmt = 'psql' , headers = 'keys', showindex = False))
       else:
              print("Wrong book Id")



#MEMBER DETAILS METHOD

def memberInput():
    try:
        memberId = int(input("Enter Member Id: "))
        memberName = input("Enter Member Name: ")
        memberAddress = input ("Enter Member Address: ")
        phNo = input("Enter Phone Number: ")
        qry = "Insert into members values({},'{}','{}','{}')".format(memberId,memberName,memberAddress,phNo)
        cursor.execute(qry)
        con.commit()
        print("Added Successfully....")

    except:
        print("Error... Wrong Entry")

def memberEdit():
       x= int(input("Enter Member Id: "))
       qry = "select * from members where memberId = {}".format(x)
       cursor.execute(qry)
       r = cursor.fetchone()
       if r:
              y = input("Enter New Address: ")
              qry = "update members set memberAddress = '{}' where memberId = {}".format(y,x)
              cursor.execute(qry)
              con.commit()
              print("Edited Successfully... ")
       else:
              print("Wrong Member Id")


def memberDelete():
       x= int(input("Enter Member Id: "))
       qry = "select * from members where memberId = {}".format(x)
       cursor.execute(qry)
       r = cursor.fetchone()
       if r:
              qry = "delete from members where memberId = {}".format(x)
              cursor.execute(qry)
              con.commit()
              print("Deleted Successfully... ")
       else:
              print("Wrong member Id")

def memberSearch():
       x= int(input("Enter Member Id: "))
       qry = "select * from members where memberId = {}".format(x)
       cursor.execute(qry)
       r = cursor.fetchone()
       if r:
              
              df = pd.read_sql(qry,con)
              print(tabulate(df, tablefmt = 'psql' , headers = 'keys', showindex = False))
       else:
              print("Wrong Member Id")


#TRANSACTION METHOD (BOOKISSUE AND BOOK RETURN)

def bookIssue():
       q = "select max(issueId) from issue"
       cursor.execute(q)
       r = cursor.fetchone()[0]
       if r:
              issueId = r + 1
       else:
              issueId = 1

       x = int(input("Enter Member Id: "))
       qr1 = "select * from members where memberId = {}".format(x)
       cursor.execute(qr1)
       r = cursor.fetchone()
       if r:
              y = int(input("Enter Book Id: "))
              qr2 = "Select bookId, remainingCopies from book where bookId = {}".format(y)
              cursor.execute(qr2)
              r = cursor.fetchone()

              if r:
                     if r[1] > 0:
                            issueDate = input("Enter Issue Date: ")
                            copies = int(input("Enter No of Copies: "))
                            remainingCopies = r[1] - copies
                            qr3 = "insert into issue values({},'{}',{},{},{})".format(issueId, issueDate, x , y , copies)
                            cursor.execute(qr3)
                            qr4 = "update book set remainingCopies = {} where bookId = {}".format(remainingCopies,y)
                            cursor.execute(qr4)
                            con.commit()
                            print("Book Issued Successfully...")
                     else:
                            print("Book is not Available...")
              else:
                     print("Wrong Book Id")
       else:
              print("Wrong Member Id")




def bookReturns():
       q = "select max(returnId) from returns"
       cursor.execute(q)
       r = cursor.fetchone()[0]
       if r:
              returnId = r + 1
       else:
              returnId = 1

       x = int(input("Enter Member Id: "))
       qr1 = "select * from members where memberId = {}".format(x)
       cursor.execute(qr1)
       r = cursor.fetchone()
       if r:
              y = int(input("Enter Book Id: "))
              qr2 = "Select bookId, remainingCopies from book where bookId = {}".format(y)
              cursor.execute(qr2)
              r = cursor.fetchone()

              if r:
                     
                     returnDate = input("Enter Return Date: ")
                     copies = int(input("Enter No of Copies: "))
                     remainingCopies = r[1] + copies
                     qr3 = "insert into returns values({},'{}',{},{},{})".format(returnId, returnDate, x , y , copies)
                     cursor.execute(qr3)
                     qr4 = "update book set remainingCopies = {} where bookId = {}".format(remainingCopies,y)
                     cursor.execute(qr4)
                     con.commit()
                     print("Book Returned Successfully...")
                     
              else:
                     print("Wrong Book Id")
       else:
              print("Wrong Member Id")

#REPORT METHOD 

def bookOutput():
       df = pd.read_sql("select * from book",con)
       print(tabulate(df,  tablefmt = 'psql', headers = 'keys', showindex = False))

def memberOutput():
       df = pd.read_sql("select * from members",con)
       print(tabulate(df,  tablefmt = 'psql', headers = 'keys', showindex = False))

def returnOutput():
       df = pd.read_sql("select * from returns",con)
       print(tabulate(df,  tablefmt = 'psql', headers = 'keys', showindex = False))

def issueOutput():
       df = pd.read_sql("select * from issue",con)
       print(tabulate(df,  tablefmt = 'psql', headers = 'keys', showindex = False))



def bookChart():
       q = "select bookId, count(copies) as totalcopies from issue group by bookId"
       df = pd.read_sql(q,con)
       print(df)
       plt.bar(df.bookId, df.totalcopies)
       plt.xlabel("Book ID")
       plt.ylabel("Copies Issued")
       plt.title("Book Ranking")
       plt.xticks(df.bookId)
       plt.show()
       


              
while (True):



    #HOME SECTION


       
    print("="*160)
    print("                                                       .....Welcome to Library Management System.....               ")
    print("="*160)
    

    print('''\t\tHOME \n\t\t\t\t\t\t\t\tEnter Your Choice ....\n\n\t\t\t\t\t1: Book Details     (Add, Edit, Delete, Search) \n\t\t\t\t\t2: Member Details   (Add, Edit, Delete,Search)   \n\t\t\t\t\t3: Transaction      (Issue , Return) \n\t\t\t\t\t4: Report           (Show List Of books, Members  and Charts)\n\t\t\t\t\t5: Exit \n''')
    choice = int(input())


    #BOOK DETAILS METHOD CALLING
    if choice == 1:
        while(True):
           print("\t\t\t\t\t\t\t\tEnter Your Choice \n\t\t\t\t\t1: Add Book Details  \n\t\t\t\t\t2: Edit Book Details \n\t\t\t\t\t3: Delete a Book \n\t\t\t\t\t4: Search a Book \n\t\t\t\t\t5: Back to Home\n")

           ch = int(input())
           if ch == 1:
              bookInput()
           elif ch == 2:
              bookEdit()
           elif ch == 3:
              bookDelete()
           elif ch == 4:
              bookSearch()
           elif ch == 5:
              break

    #MEMBER DETAILS METHOD CALLING

    elif choice == 2:
       while(True):
           print("\t\t\t\t\t\t\t\tEnter Your Choice \n\t\t\t\t\t1: Add Member Details  \n\t\t\t\t\t2: Edit Member Details \n\t\t\t\t\t3: Delete a Member \n\t\t\t\t\t4: Search a Member \n\t\t\t\t\t5: Back to Home\n")

           ch = int(input())
           if ch == 1:
              memberInput()
           elif ch == 2:
              memberEdit()
           elif ch == 3:
              memberDelete()
           elif ch == 4:
              memberSearch()
           elif ch == 5:
              break

    #TRANSACTION METHOD CALLING FOR ISSUE AND RETURN

            
    elif choice == 3:
       while(True):
           print("\t\t\t\t\t\t\t\tEnter Your Choice \n\t\t\t\t\t1: Issue Book  \n\t\t\t\t\t2: Retun Book \n\t\t\t\t\t3: Back to Home\n")

           ch = int(input())
           if ch == 1:
              bookIssue()
           elif ch == 2:
              bookReturns()
           elif ch == 3:
              break

    #REPORT METHOD CALLING 
          
    elif choice == 4:
        while(True):
          print("\t\t\t\t\t\t\t\tEnter Your Choice \n\t\t\t\t\t1: Book Details  \n\t\t\t\t\t2: Member Details \n\t\t\t\t\t3: Issue Details \n\t\t\t\t\t4: Return Details \n\t\t\t\t\t5: Book Ranking(CHART) \n\t\t\t\t\t6: Back to Home\n")
          ch = int(input())
          if ch == 1:
              bookOutput()
          elif ch == 2:
              memberOutput()
          elif ch == 3:
              issueOutput()
          elif ch == 4:
              returnOutput()
          elif ch == 5:
              bookChart()
          elif ch == 6:
              break
    elif choice == 5:
       break





