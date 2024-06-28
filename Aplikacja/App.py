import AppHandlers
import DBHandling as DB
# import simplejson
import sqlite3
# import psycopg

# with open("database_creds.json") as db_con_file:
#    creds = simplejson.loads(db_con_file.read())

# conn = psycopg.connect(
#     dbname =creds['db_name'],
#     user =creds['user_name'],
#     password= creds['password'],
#     host =creds['host_name'],
#     port =creds['port_number']
# )
# cursor = conn.cursor()
con = sqlite3.connect("temp.db")
c = con.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS BookList (
        Name TEXT,
        Surname TEXT,
        Title TEXT,
        Price INTEGER,
        Page INTEGER,
        CoO TEXT,
        Copies INTEGER,
        UNIQUE (Title)
    )''')

LibraryDict = {}
i = 0;
while True:
    print("Please select type of action\n")
    choice = input("1. To add new entry:\n2. To Save\n3. Switch to data placed Online\n4. End the program\n")
    match choice:
        case "1":
            print("Adding new entry")
            print("Author:")
            data = AppHandlers.AddBook() 
            LibraryDict.update({i : data})
            print(LibraryDict)
            i+=1
        case "2":
            print("Saveing the data localy")
            if not bool(LibraryDict):
                print ("No data to save!")
                continue
            AppHandlers.SaveAsCsv (LibraryDict)
        case "3":
            # DB.ClearDB(con,c)
            DB.CSVtoDB(con,c)
            print ("Printing data placed online")
            DB.DeleteBook(con,c,'Ptaki nocy ')
            DB.PrintTable(con,c)
            DB.AddBook(con,c,["Hubert","Albanowski","Niesamowite Krzemy Tomczaka", 12, 127, "Poland",2])
            print()
            DB.PrintTable(con,c)
            DB.UpdateCopies(con,c,"Niesamowite Krzemy Tomczaka", 3)
            print()
            DB.PrintTable(con,c)
            DB.ExportAsCSV(con,c)
        case "4":
            con.close()
            print ("Ending and closing")
            break
