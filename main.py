#FEW FUNCTIONS FOR CODE-

def do_a_booking():

    while True:
        
        import mysql.connector
        r=input("enter Show_ID")
        db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
        cursor=db.cursor()
        Query1=("select shows.movie_id, timings,hall_no,movies.movie_name from shows,movies where show_id='%s' and movies.movie_id=shows.movie_id" %(r))
        cursor.execute(Query1)
        result=cursor.fetchall()
        
        if not result:
            print("No such show exists")
            cursor.close()
            
        else:
            print("\nDetails of the show\n")
            for i in result:
                print(i[0],i[1],i[2],i[3])
            
            print("\nEnter customer details:")
            s=input("enter a user id for you: ")
            
            f=input("enter date you wanna watch the movie (YYYY-MM-DD)")

            while True:        
                u=input("enter your seat type: (G/P/S) G: Gold, P: Platinum, S: Silver}")
                if  not (u=="G" or u=="P" or u=="S"):
                    print("Enter only G or P or S")
                else:
                    
                    if (u=="S"):
                        Q=("select G from seat_cat where movie_id=(select movie_id from shows where show_id='%s')" %(r))
                        while True:
                            t=input("\nEnter the row of your seat: (A/B/C/D/E) - A being closest to the screen")
                            if  not (t=="A" or t=="B" or t=="C" or t=="D" or t=="E"):
                                print("Enter only A or B or C or D or E")
                            else:
                                while True:
                                    t1=int(input("Enter your seat number (no. btw 1(leftmost) to 10(rightmost) )"))
                                    if not (t1>=1 and t1<=10):
                                        print("Enter a no. btw 1 and 10")
                                    else:
                                        break
                                break        
                            
                    elif (u=="G"):
                        Q=("select S from seat_cat where movie_id=(select movie_id from shows where show_id='%s')" %(r))
                        while True:
                            t=input("\nEnter the row of your seat: (F/G/H/I) - F being closest to the screen")
                            if  not (t=="F" or t=="G" or t=="H" or t=="I"):
                                print("Enter only F or G or H or I")
                            else:
                                while True:
                                    t1=int(input("Enter your seat number (no. btw 1(leftmost) to 10(rightmost) )"))
                                    if not (t1>=1 and t1<=10):
                                        print("Enter a no. btw 1 and 10")
                                    else:
                                        break
                                break
                           
                    else:
                        Q=("select P from seat_cat where movie_id=(select movie_id from shows where show_id='%s')" %(r))
                        while True:
                            t=input("\nEnter the row of your seat: (J/K/L) - L being farest from the screen")
                            if  not (t=="J" or t=="K" or t=="L" ):
                                print("Enter only J or K or L")
                            else:
                                while True:
                                    t1=int(input("Enter your seat number (no. btw 1(leftmost) to 10(rightmost) )"))
                                    if not (t1>=1 and t1<=10):
                                        print("Enter a no. btw 1 and 10")
                                    else:
                                        break
                                break

                    seat_no=t+str(t1)      
                    
                    cursor.execute(Q)
                    seat_price=cursor.fetchone()
                    # print(seat_price[0])
                    
                    break

            
            print("\nThis is your booking:\n","\nMOVIE_ID:",result[0][0],"\nSHOW_ID:",r,"\nSEAT TYPE:",u,"\nHALL_NO:",result[0][2],"\nTIMINGS:",result[0][1],"\nDATE:",f,"\nSEAT_NO:",seat_no,"\nSEAT PRICE:",seat_price[0],"\nUSER_ID:",s)
           
            o=input("\nAre you sure you want to confirm this booking? (Y/N)")

            if o!="Y":
                break
            
            else:

                Query=("insert into bookings values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                data=(result[0][0],r,u,result[0][2],result[0][1],f,seat_no,seat_price[0],s)
                cursor.execute(Query,data)
                db.commit()
                print("Your booking has been confirmed.\n")
                
                cursor.close()

                break


def plotter():
    
       
    import mysql.connector
    import matplotlib.pyplot as plt
    import numpy as np
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    Query1=("select P,G,S from seat_cat")
    cursor.execute(Query1)
    res=cursor.fetchall()

    a=[]
    m=[]
    c=[]
    for i in res:
        a.append(i[0])
        m.append(i[1])
        c.append(i[2])

    Query2=("select left(movie_name,11) from movies,seat_cat where seat_cat.movie_id=movies.movie_id")
    cursor.execute(Query2)
    rees=cursor.fetchall()

    b=[]
    for j in rees:
        b.append(j[0])
    barwidth=0.2
    q=np.arange(len(a))
    p= [k+barwidth for k in q]
    o= [l+barwidth for l in p]
    plt.bar(q,a,barwidth,color="orange")
    plt.bar(p,m,barwidth)
    plt.bar(o,c,barwidth,color="pink")
    
    plt.title("Prices across various seats",color="purple",fontsize=13)
    plt.ylabel("Price in Rupees Silver vs Gold vs Platinum ",color="purple",fontsize=11)
    plt.xlabel("Movie Name",color="purple",fontsize=11)
    

    plt.xticks(q+barwidth,b)
    plt.show()
        



def all_shows():

    import mysql.connector
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    cursor.execute("select  movies.movie_id ,left(movie_name,11), duration,language,format,genre,certification, DATE_FORMAT(release_date,'%d/%m/%Y'),timings,S,G,P from movies,shows,seat_cat where movies.movie_id=seat_cat.movie_id and shows.movie_id=movies.movie_id")
    result=cursor.fetchall()

    print("{0:10}{1:15}{2:10}{3:7}{4:7}{5:7}{6:8}{7:13}{8:8}{9:5}".format("========"," ==========","========","====","======"," ===== ","  =======  ","============"," ======="," =================================")) 
    print("{0:10}{1:15}{2:10}{3:7}{4:7}{5:7}{6:8}{7:13}{8:8}{9:5}".format("Movie ID"," Movie Name","Duration","Lang","Format"," Genre ","  Certify  ","Release_Date"," Timings"," Seat Prices:Silver,Gold,Platinum"))
    print("{0:10}{1:15}{2:10}{3:7}{4:7}{5:7}{6:8}{7:13}{8:8}{9:5}".format("========"," ==========","========","====","======"," ===== ","  =======  ","============"," ======="," =================================")) 

    for x in result:
        # for i in len(x):
        #     print(x[i])
        print ("{0:11}{1:15}{2:10}{3:7}{4:7}{5:10}{6:3}".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]),"  ",x[7],"  ","{0:7}{1:8}{2:8}{3:8}".format(x[8],x[9],x[10],x[11]))
        # print(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11] {7:10}{8:8}{9:5}{10:5}{11:5})
    cursor.close()

    
def add_a_show():

    import mysql.connector

    h=input("enter show id")
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    Query1=("select * from shows where show_id='%s'" %(h))
    cursor.execute(Query1)
    res=cursor.fetchall()
    
    if not res:
        while True:
            q=int(input("Menu options\n1. Enter new movie\n2.Enter a new show for an existing movie"))
            if (q==1):
                r=input("enter new movie id ")
                cursor=db.cursor()
                Query11=("select * from movies where movie_id='%s'" %(r))
                cursor.execute(Query11)
                res=cursor.fetchall()
                if not res:
                    aa=input("enter name of movie ")
                    b=input("enter durtion of the movie")
                    c=input("enter language")
                    ff=input("enter format")
                    g=input("enter genre ")
                    i=input("enter certification")
                    j=input("enter release date (YYYY-MM-DD)")
                    Query=("insert into movies values(%s,%s,%s,%s,%s,%s,%s,%s)")
                    data=(h,aa,b,c,ff,g,i,j)
                    cursor.execute(Query,data)
                    db.commit()

                    a=input("enter time of show ")
                    e=int(input("enter hall/audi number (1/2/3/4)"))
                    Quer=("insert into shows values(%s,%s,%s,%s)")
                    f="A"+str(e)
                    dat=(h,r,a,f)
                    cursor.execute(Quer,dat)
                    db.commit()

                    print("New Show with show_id '%s' has been successfully added." %(h))

                    cursor.close()
                else:
                    print("Such a movie already exists")
                break
            elif (q==2):
                r=input("enter existing movie's id ")
                cursor=db.cursor()
                Query11=("select * from shows where movie_id='%s'" %(r))
                cursor.execute(Query11)
                rs=cursor.fetchall()
                if rs:
                    a=input("enter time of show ")
                    e=int(input("enter hall/audi number (1/2/3/4)"))
                    f="A"+str(e)
                    Query=("insert into shows values(%s,%s,%s,%s)")
                    data=(h,r,a,f)
                    cursor.execute(Query,data)
                    db.commit()

                    print("New Show with show_id '%s' has been successfully added." %(h))

                    cursor.close()
                else:
                    print("Such a movie doesnt exist")
                break
            else:
                print("enter only 1 or 2")
        
        
    else:    

        print("Such a show already exists")
        cursor.close()

    
def edit_a_show():

    q=int(input("Enter 1 to edit a show's timing or audi\n Enter 2 to edit a movie's details "))
    import mysql.connector        
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    if (q==1):
        r=input("enter show id")
        Query1=("select * from shows where show_id='%s'" %(r))
        cursor.execute(Query1)
        res=cursor.fetchall()
        
        if not res:

            print("No such show exists")

            cursor.close()

        else:

            print("MENU OF FIELDS","\n","1.TIMING","\n","2.AUDI NUMBER","\n")
            m=int(input("Enter your choice of field which you wish to update:"))
            o={1:'timings',2:'hall_no'}
            q=o.get(m)
            n=input("Enter new value:")
            
            Query=("update shows set %s='%s' where show_id='%s'"%(q,n,r))
            cursor.execute(Query)
            db.commit()

            print("\nFor show with id '%s', the '%s' has been successfully updated to '%s'."%(r,q,n))
    elif (q==2):
        r=input("enter movie id")
        Query1=("select * from movies where movie_id='%s'" %(r))
        cursor.execute(Query1)
        res=cursor.fetchall()
        
        if not res:

            print("No such movie exists")

            cursor.close()

        else:

            print("MENU OF FIELDS","\n","1.MOVIE NAME","\n","2.DURATION","\n","3.LANGUAGE","\n","4.FORMAT","\n","5.GENRE","\n","6.CERTIFICATION","\n","7.RELEASE_DATE")
            m=int(input("Enter your choice of field which you wish to update:"))
            o={1:'movie_name',2:'duration',3:'language',4:'format',5:'genre',6:'certification',7:'release_date'}
            q=o.get(m)
            n=input("Enter new value:")
            
            Query=("update movies set %s='%s' where movie_id='%s'"%(q,n,r))
            cursor.execute(Query)
            db.commit()

            print("\The '%s' ,for the movie with id '%s', has been successfully updated to '%s'."%(q,r,n))
    else:
        print("Enter only 1 or 2")
            
            
    cursor.close()

        
def delete_a_show():

    import mysql.connector

    r=input("enter show id")
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    Query1=("select * from shows where show_id='%s'" %(r))
    cursor.execute(Query1)
    res=cursor.fetchall()

    if not res:

        print("No such show exists")
        

    else:
        query2=("select count(*) from bookings where show_id='%s'" %(r))
        cursor.execute(query2)
        rs=cursor.fetchall()

        if (rs[0][0])>0:
            
            print("This show can not be deleted because a booking already exists.")

        else:

            Query=("delete from shows where show_id='%s'" %(r))
            cursor.execute(Query)
            db.commit()

            print("The show '%s' has been successfully deleted."%(r))

            cursor.close()

def delete_a_movie():

    import mysql.connector

    r=input("enter movie id")
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    Query1=("select * from movies where movie_id='%s'" %(r))
    cursor.execute(Query1)
    res=cursor.fetchall()

    if not res:

        print("No such movie exists")
        

    else:
        query2=("select count(*) from shows where movie_id='%s'" %(r))
        cursor.execute(query2)
        rs=cursor.fetchall()

        if (rs[0][0])>0:
            
            print("This movie can not be deleted because a show already exists.")

        else:

            Query=("delete from movies where movie_id='%s'" %(r))
            cursor.execute(Query)
            db.commit()

            print("The movie with movie id '%s' has been successfully deleted."%(r))

            cursor.close()

def view_one_booking():
    r=input("Enter user id ")
    import mysql.connector
    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    
    cursor.execute("select * from bookings where user_id='%s'" %(r))
    reesult=cursor.fetchall()
    if not reesult:
        print("no booking exists for this user")
    else:
        
        print("{0:10}{1:10}{2:10}  {3:8} {4:11}{5:13}{6:7} {7:7}{8:10}".format("========","========","==========","=======","=======","==========","========"," ====="," ========"))
        print("{0:10}{1:10}{2:10}  {3:8} {4:11}{5:13}{6:7}   {7:7}{8:10} ".format("MOVIE_ID","SHOW_ID","SEAT_TYPE","HALL_NO","TIMINGS","BOOK_DATE","SEAT_NO","FARE","USER_ID"))
        print("{0:10}{1:10}{2:10}  {3:8} {4:11}{5:13}{6:7} {7:7}{8:10} ".format("========","========","==========","=======","=======","==========","========"," ====="," ========"))

        for x in reesult:
            
            print("{0:10}{1:10}{2:10}  {3:8} {4:10}".format(x[0],x[1],x[2],x[3],x[4]),x[5],"  ","{0:8}".format(x[6]),x[7],"  ","{0:8}".format(x[8]))

    

    
    cursor.close()

def all_bookings():

    import mysql.connector

    db=mysql.connector.connect(host='localhost',user='root',password='1234',database='bpower')
    cursor=db.cursor()
    #cursor.execute(" select * from bookings")
    cursor.execute(" select MOVIE_ID,SHOW_ID,SEAT_TYPE,HALL_NO,TIMINGS,DATE_FORMAT(book_date,'%d/%m/%Y'),SEATNO,price,USER_ID from bookings")
    reesult=cursor.fetchall()

    print("{0:10}{1:10}{2:10}  {3:8} {4:11}{5:13}{6:7} {7:7}{8:10}".format("========","========","==========","=======","=======","==========","========"," ====="," ========"))
    print("{0:10}{1:10}{2:10}  {3:8} {4:11}{5:13}{6:7}   {7:7}{8:10} ".format("MOVIE_ID","SHOW_ID","SEAT_TYPE","HALL_NO","TIMINGS","BOOK_DATE","SEAT_NO","FARE","USER_ID"))
    print("{0:10}{1:10}{2:10}  {3:8} {4:11}{5:13}{6:7} {7:7}{8:10} ".format("========","========","==========","=======","=======","==========","========"," ====="," ========"))

    for x in reesult:
         
        print("{0:10}{1:10}{2:10}  {3:8} {4:10}".format(x[0],x[1],x[2],x[3],x[4]),x[5],"  ","{0:8}".format(x[6]),x[7],"  ","{0:8}".format(x[8]))

    cursor.close()

    
#MAIN CODE-


while True:
    
    print("****************************** \nWELCOME TO OUR B TEAM CINEMAS \n******************************","\n")
    
    a=input("Are you a Customer or an Admin?(C/A)")

    if a=="C":

        print("\n Welcome Customer!","\n")
        
        while True:

            try:

                print("--------------------------------\nCustomer Menu:\n-------------------------------- \n 1.Available shows","\n","2.View your booking","\n","3.Book a seat in a show","\n","4.Exit from Customer Menu","\n","5.Exit from the Cinema System","\n")

                b=int(input("Enter your choice: (1/2/3/4/5)\n"))

                if b==1:
                    all_shows()
                    
                elif b==2:

                    view_one_booking()
                elif b==3:
                    do_a_booking()
                elif b==4:
                    break
                elif b==5:
                    print("Goodbye")
                    quit()
                
                else:
                    print("Enter a number between 1 to 5 only")                                    

            except(ValueError,TypeError,NameError):
                print("Enter correct values")

    elif a=="A":

        while True:
            pwrd=input("enter password")

            if pwrd=="btnt":
                print("\n","Welcome Administrator!","\n")
                
                while True:

                    try:

                        print("-----------------------------------\nAdmin Menu: \n----------------------------------- \n 1.Available shows","\n","2.Plot of prices across various seats","\n","3.Add a new show or a new movie","\n","4.Edit a show or a movie","\n","5.Delete a show of a movie","\n","6.Delete a movie","\n","7.View all bookings","\n","8.Exit from Admin Menu","\n","9.Exit from the Cinema System","\n")
                        c=int(input("Enter your choice: (1/2/3/4/5/6/7/8/9) \n"))

                        if c==1:
                            all_shows()
                        elif c==2:
                            plotter()
                        elif c==3:
                            add_a_show()
                        elif c==4:
                            edit_a_show()
                        elif c==5:
                            delete_a_show()
                        elif c==6:
                            delete_a_movie()
                        elif c==7:
                            all_bookings()
                        elif c==8:
                            break
                        elif c==9:
                            print("Goodbye")
                            quit()
                        else:
                            print("Enter a number between 1 to 9 only")                                            

                    except(ValueError,TypeError,NameError):
                        print("enter correct values")
                break

            else:
                print("Incorrect password.","\n")   
                    

    else:
        print("Enter only A or C")
