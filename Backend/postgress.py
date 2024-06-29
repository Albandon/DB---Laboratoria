import csv
import psycopg
import simplejson

def Init (conJSON):
    con = psycopg.connect(
        host=conJSON['host'],
        port=conJSON['port'],
        user=conJSON['user'],
        dbname=conJSON['db_name'],
        password=conJSON['password']
    )
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS BookList (
        Name VARCHAR(30),
        Surname VARCHAR(30),
        Title VARCHAR(60) UNIQUE,
        Page INT,
        CountryOfOrigin VARCHAR(3),
        Copies INT,
        )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Clients (
        Name VARCHAR(30),
        Surname VARCHAR(30),
        LibraryID INT UNIQUE,
        LoanedTitle VARCHAR(60) REFERENCES BookList(Title)
        )''')
    con.commit()
    c.close()
    con.close()

def CSVtoDB (BookFile, ClientFile, conJSON):
    con = psycopg.connect(
        host=conJSON['host'],
        port=conJSON['port'],
        user=conJSON['user'],
        dbname=conJSON['db_name'],
        password=conJSON['password']
    )
    c = con.cursor()

    try: 
        with open(BookFile,"r") as f:
            reader = csv.reader(f)
            for row in reader:
                data = next(reader)
                print(row)
                c.execute('''INSERT INTO BookList (Name, Surname, Title, Page, CountryOfOrigin, Copies) 
                          VALUES (%s,%s,%s,%s,%s,%s);''' (data))
        with open(ClientFile,"r") as f:
            reader = csv.reader(f)
            for row in reader:
                data = next(reader)
                print(row)
                c.execute('''INSERT INTO Clients (Name, Surname, LibraryID, LoanedTitle) 
                          VALUES (%s,%s,%s,%s);''' (data))      
    except Exception as ex:
        print(f"Exception: {ex}")

with open ("./db_creds.json") as f:
    db_creds = simplejson.load(f)
    Init(db_creds)
    CSVtoDB("../Aplikacja/Books.csv","../Aplikacja/Clients.csv",db_creds)
