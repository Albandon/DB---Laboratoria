
import AppHandlers
import DBHandling as DB
import sqlite3

con = sqlite3.connect("temp.db")
c = con.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS BookList (
        Name TEXT,
        Surname TEXT,
        Title TEXT,
        Page INTEGER,
        CountryOfOrigin TEXT,
        Copies INTEGER,
        UNIQUE (Title)
    )''')

c.execute('''CREATE TABLE IF NOT EXISTS Clients (
          Name TEXT,
          Surname TEXT,
          LibraryID INTEGER,
          LoanedTitle TEXT,
          UNIQUE (LibraryID)
          )''')

LibraryDict = {}
i = 0;
# DB.CSVtoDB(con,c,"Books","Clients")
while True:
    print("Please select type of action\n")
    choice = input("1. To add new entry:\n2. Lend book: \n3. To Save\n4. Switch to database mode\n5. End the program\n")
    try:
        match choice:
            case "1":
                print("Adding new entry")
                print("Author:")
                data = AppHandlers.BookHandler()
                DB.AddBook(con, c, data)
            case "2":
                print("Adding new Client")
                print("Loander: ")
                data = AppHandlers.ClientHandler()
                DB.AddLoanEntry(con,c,data)
            case "3":
                print("Saveing the data to csv")
                DB.ExportAsCSV(con,c)
            case "4":
                DB.DatabaseMode(con,c)
            case "5":
                c.close()
                con.close()
                print ("Ending and closing")
                break
    except Exception as ex:
        print(f"Exception occured: {ex}")

