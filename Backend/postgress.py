import csv
import psycopg
import simplejson
import random

def Init (conJSON):
    """Łączy się z podaną bazą daych oraz inicjalizuje tabele na postgreSQL.
    
    :param conJSON: załadowany plik .json zawierający dane połącznia 
    :type conJSON: dict
    
    """
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
        Copies INT
        );''')
    # use of Serial to gen ID? -> would need some changes like separate table for clients with just id and name, surname -> table with just id that references and title but i don't care for that this much
    c.execute('''CREATE TABLE IF NOT EXISTS Clients (
        Name VARCHAR(30),
        Surname VARCHAR(30),
        LibraryID INT, 
        LoanedTitle VARCHAR(60) REFERENCES BookList(Title)
        );''')

    con.commit()
    c.close()
    con.close()

# dla ułatwienia randomizacji ilość kopii nie będzie zmieniania dodając nowe wpisy do wypożyczeń
def buildRandomLoanData (n: int, conJSON):
    """ Przygotowuje zadaną ilość danych i wprowadza je do tabeli kilentów. Ważne jest by istniała wcześniej tabela `BookList` ze wszystkimi potrzebnymi tytułami
    
    :param n: Ilość danych
    :type n: int
    :param conJSON: załadowany plik .json zawierający dane połącznia 
    :type conJSON: dict
    
    """
    con = psycopg.connect(
        host=conJSON['host'],
        port=conJSON['port'],
        user=conJSON['user'],
        dbname=conJSON['db_name'],
        password=conJSON['password']
    )
    c = con.cursor()
    c.execute('''SELECT LibraryID FROM Clients''')

    TakenIDs = [x[0] for x in c.execute('''SELECT LibraryID FROM Clients''').fetchall()]
    Names = ["Janek","Tomasz","Janusz","Mariusz","Szymon","Adam","Kuba","Janusz"]
    Surnames = ["Kowalski","Polczak","Januszkiewicz","Jurgiel","Wójcik","Dąbrowski","Kamiński","Wiśniewski","Raczyk","Mazowiecki"]
    Titles = ["Niesamowite Krzemy Tomczaka","8 centow - historia prawdziwa","Poznan nie placze","I Had some Help","Juz nie moge","Jak zostac Papiezem","Wladca obraczek","Tamten Nieznajomy","Hioppit","Moby Dykt"]
    while n > 0:
        Name = random.choice(Names)
        Surname = random.choice(Surnames)
        Title = random.choice(Titles)
        ID = random.randint(100_000,999_999)
        if not ID in TakenIDs:
            n = n-1
            TakenIDs.append(ID)
            c.execute('''INSERT INTO Clients (Name, Surname, LibraryID, LoanedTitle) 
                      VALUES (%s,%s,%s,%s);''',(Name,Surname,ID,Title))
    con.commit()
    c.close()
    con.close()

def CSVtoDB (BookFile, ClientFile, conJSON):
    """ Importuje dane z plików .csv do bazy danych na postgresie. Wymaga storzonych tabeli `BookList` oraz `Clients`, należy więc wcześniej wykonać metodę **Init ()**
    
    :param BookFile: Nazwa, wraz z rozszerzeniem
    :type BookFile: 'Book.csv'
    :param ClientFile: Nazwa, wraz z rozszerzeniem
    :type BookFile: 'Clients.csv'
    :param conJSON: załadowany plik .json zawierający dane połącznia 
    :type conJSON: dict
    
    """
    
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
    c.close()
    con.close()



#with open ("database_creds.json") as f:
 #   db_creds = simplejson.load(f)
  #  Init(db_creds)
   # CSVtoDB("Books.csv","Clients.csv",db_creds)
