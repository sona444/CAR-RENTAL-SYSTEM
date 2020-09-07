import hashlib as hasher
import datetime as date
import sqlite3

conn=sqlite3.connect('cars.sqlite')
cur=conn.cursor()
class block:
    def __init__(self, indexx, timestamp, owner,car_number, previous_hash):
        self.indexx=indexx
        self.timestamp=timestamp
        self.owner=owner
        self.car_number=car_number
        self.previous_hash=previous_hash
        self.hash=self.proof_of_work()
        

    def hash_block(self):
        sha=hasher.sha256()
        sha.update(str(self.indexx).encode('UTF-8') + str(self.timestamp).encode('UTF-8') + str(self.owner).encode('UTF-8') + str(self.previous_hash).encode('UTF-8') + str(self.nonce).encode('UTF-8')) 
        return sha.hexdigest()

    
    def proof_of_work(self):
        found=False
        self.nonce=0
        while found==False:
            block_hash=str(self.hash_block())
            if block_hash.startswith('0000'):
                found=True
            self.nonce+=1
            block_hash=str(self.hash_block())
        cur.execute('''UPDATE BLOCK SET HASH=?, NONCE=? WHERE BLOCK_ID=(SELECT MAX(BLOCK_ID) FROM BLOCK);''',(block_hash, self.nonce))
        conn.commit()
        return block_hash, self.nonce

##def create_genesis_block():
##    return block(0,date.datetime.now(),"I am genesis Block",NULL,"Sonakshi","0")


def next_block(last_block,owner_name, car_number):
    next_index = int(last_block[1]) + 1
    next_timestamp = date.datetime.now()
    next_data = owner_name
    next_carNumber=car_number
    next_hash = last_block[7]
    cur.execute("INSERT INTO BLOCK (INDEX_1, TIMESTAMP, OWNER_NAME, PREVIOUS_HASH, CAR_NUMBER ) VALUES (?,?,?,?,?)",(next_index, next_timestamp, next_data, next_hash, next_carNumber))
    conn.commit()
    return block(next_index, next_timestamp, next_data, next_carNumber, next_hash)



choice=input("Do You Want To Earn From Your Idle Car???(y/n)")
if choice=='y':
    name=input("Enter your name")
    cur.execute(' SELECT CAR_ID, CAR_NAME FROM CARS')
    rows=cur.fetchall()
    print("(car_ID, car_name)")
    for row in rows:
        print(row)
    ID=input("Choose Car ID corresponding to your Car Model if not available enter N")
    if ID=='N':
        car_model=input("Enter full name of your car")
        amount=input("Enter your expected rent for the car upto 150 kms")
        cur.execute("INSERT INTO CARS (CAR_NAME, PRICE_WITH_FUEL,PRICE_WITHOUT_FUEL) VALUES (?,?,?)",(car_model,amount,amount,))
        conn.commit()
    else:
        cur.execute("SELECT CAR_NAME FROM CARS WHERE CAR_ID=(?)",(ID,))
        car_model=cur.fetchone()
        print(car_model,"registered")
        cur.execute("SELECT CAR_NAME FROM CARS WHERE CAR_ID=(?)",(ID,))
        amount2=cur.fetchone()
        cur.execute("SELECT CAR_NAME FROM CARS WHERE CAR_ID=(?)",(ID,))
        amount3=cur.fetchone()
    car_number=input("Enter Your Car Number")
    location=input("Enter Your City")
    phone=input("Enter Your Mobile Number")
    Email=input("Enter Your Email Id")
    availability=input("Enter The Week's day when your car is available")
    duration=input("Enter the duration (Eg:2:00PM-7:00PM)")
    cur.execute("INSERT INTO OWNER (NAME, CAR_MODEL, CAR_NUMBER, LOCATION, PHONE_NUMBER, EMAIL_ID,AVAILABILITY, DURATION) VALUES (?,?,?,?,?,?,?,?)",[str(name), str(car_model), str(car_number), str(location), int(phone), str(Email), str(availability), str(duration)])
    cur.execute("SELECT * FROM BLOCK WHERE BLOCK_ID=(SELECT MAX(BLOCK_ID) FROM BLOCK);")
    previous_block=cur.fetchall()[0]
    print(previous_block)
    next_block(previous_block, name, car_number)
    cur.execute("UPDATE BLOCK SET CAR_ID=?, CAR_NUMBER=? WHERE BLOCK_ID=(SELECT MAX(BLOCK_ID) FROM BLOCK);",(ID,car_number))
    conn.commit()
    
    
elif choice=='n':
    name=input("enter your name")
    print("If you want to rent a car these are the available cars with their price")
    print("('car_id','car_name','price without fuel','price with fuel')")
    cur.execute(' SELECT * FROM "CARS";')
    rows=cur.fetchall()
    for row in rows:
        print(row)
    get=input("Enter the car's ID in which you are interested\n")
    cur.execute("SELECT * FROM CARS WHERE CAR_ID=(?)",(get,))
    rows=cur.fetchone()
    print(rows)
    print(rows[1],"selected")
    choice1=input("enter 1 for car with fuel and 2 for car without fuel")
    if choice1==1:
        amount=rows[1]
    else:
        amount=rows[2]
    print("you have to pay", amount)
    license_no=input("enter your license number")
    adhar_no=input("enter your adhaar number")
    phone=input("enter your phone number")
    email=input("enter email ID")
    cur.execute("INSERT INTO CUSTOMER (NAME, DRIVING_LICENCE, ADHAAR_CARD, AMOUNT, PHONE_NO, EMAIL_ID) VALUES (?,?,?,?,?,?)",(name, license_no, adhar_no, amount, phone, email,))
    cur.execute("UPDATE BLOCK SET CUSTOMER_NAME=?, AMOUNT=? WHERE CAR_ID=?", (name, amount, get,))
    conn.commit()
conn.close()
