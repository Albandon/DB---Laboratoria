import psycopg
import simplejson

def SelectAll (connection: psycopg.connection, tableName):
    cursor = connection.cursor()
    selected = cursor.execute(f"SELECT * FROM {tableName}").fetchall()
    cursor.close()
    return selected

def Select (connection: psycopg.connection, tableName, selectionType, selection):
    cursor = connection.cursor()
    selected = cursor.execute(f"SELECT * FROM {tableName} WHERE {selectionType} = '{selection}'").fetchall()
    cursor.close()
    return selected

def SelectClientSelectionType ():
    print("\nYou can select client by: ")
    match input("1. Title\n2. Surname\n3. ID\n4. Cancel\n"):
        case "1":
            return "LoanedTitle"
        case "2":
            return "Surname"
        case "3":
            return "LibraryID"
        case "4":
            return           
        
def SelectBookSelectionType ():
    print("\nYou can select book by: ")
    match input("1. Title\n2. Author surname\n3. Cancel\n"):
        case "1":
            return "Title"
        case "2":
            return "Surname"
        case "3":
            return
    
    
def SelectTable ():
    print()
    match input("1. List of Books\n2. List of loaners\n3. Cancel\n"):
        case "1":
            return "BookList"
        case "2":
            return "Clients"
        case "3":
            return
        
with open ("database_creds.json") as f:
    db_creds = simplejson.load(f)
    con = psycopg.connect(
        host=db_creds['host'],
        port=db_creds['port'],
        user=db_creds['user'],
        dbname=db_creds['db_name'],
        password=db_creds['password']
    )       

while True:

    match input("\n1. Select all\n2. Select Specific\n3. Exit"):
        case "1":
            table = SelectTable()
            for x in SelectAll(con,table):
                print(x)
        case "2":
            table = SelectTable()
            if table == "BookList":
                Type = SelectBookSelectionType()
            if table == "Clients":
                Type == SelectClientSelectionType()
            for x in Select(con,table,Type,input("Selection: ")):
                print(x)
        case "3":
            con.close()
            break
            
