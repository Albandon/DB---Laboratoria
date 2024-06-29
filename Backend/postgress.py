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
    c.execute('''DROP TABLE Clients''')
    c.execute('''DROP TABLE BookList''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS BookList (
        Name VARCHAR(30),
        Surname VARCHAR(30),
        Title VARCHAR(60) UNIQUE,
        Page INT,
        CountryOfOrigin VARCHAR(3),
        Copies INT
        );''')
    # use of Serial to gen ID? -> would need some changes like separate table for clients with just id and name, surname -> table with just id that references and title but i don't care for that this much
    c.execute('''CREATE TABLE IF NOT EXISTS Clients (
        Name VARCHAR(30),
        Surname VARCHAR(30),
        LibraryID INT UNIQUE, 
        LoanedTitle VARCHAR(60) REFERENCES BookList(Title)
        );''')

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

    with open(BookFile,"r") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                i=i+1
                continue
            print(row)
            c.execute('''INSERT INTO BookList (Name, Surname, Title, Page, CountryOfOrigin, Copies) 
                      VALUES (%s,%s,%s,%s,%s,%s);''', (row))
    with open(ClientFile,"r") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                i=i+1
                continue
            print(row)
            c.execute('''INSERT INTO Clients (Name, Surname, LibraryID, LoanedTitle) 
                      VALUES (%s,%s,%s,%s);''', (row))
    con.commit()


with open ("database_creds.json") as f:
    db_creds = simplejson.load(f)
    Init(db_creds)
    CSVtoDB("Books.csv","Clients.csv",db_creds)