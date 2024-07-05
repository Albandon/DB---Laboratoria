import csv
import sqlite3
import AppHandlers

def CSVtoDB (connection: sqlite3.Connection, cursor: sqlite3.Cursor, file: str):
    """ Importuje dane z pliku .csv do lokalnej bazy danych
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param file: Nazwa pliku csv bez rozszerzenia
    
    """
    z = open (file + ".csv",newline='')
    reader = csv.reader(z, delimiter=',')
    for row in reader:
        cursor.execute("INSERT OR REPLACE INTO BookList VALUES (?,?,?,?,?,?)", row)
    connection.commit()

def DeleteBook (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Title):
    """Usuwa książkę na podstawie podanego tytułu, z bazy danych
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param Title: Tytuł książki
    """
    cursor.execute("DELETE FROM BookList WHERE Title = (?)", (Title,))
    connection.commit()

def DeleteEntry (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Title, tableName):
    """Usuwa podany wpis z podanej tabeli oraz o podanym tytule.
    
    Jeżeli usuwamy z tabeli wypożyczonych, stan kopi w tabeli `BookList` ulega zmianie na x+1.
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param Title: Tytuł ksiażki
    :param tableName: Nazwa tabeli
    """
    if tableName == "BookList":
        cursor.execute(f"DELETE FROM {tableName} WHERE Title = '{Title}'")
    if tableName == "Clients":
        ID = input("\tLibrary card id (6-digit)")
        cursor.execute(f"DELETE FROM {tableName} WHERE LoanedTitle = '{Title}' AND LibraryID = '{ID}'")
        selection = Select(connection,cursor,"BookList","Title",Title)
        select = [x[5] for x in selection]
        UpdateCopies(connection,cursor,Title,select[0] + 1)
    connection.commit()

def AddBook (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Book: list):
    """Dodaj nową książkę do bazy danych
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param Book: Dane książki
    :type Book: [Imię, Nazwisko, Tytuł, Ilość stron, Ilość kopii na stanie ]
    
    """
    cursor.execute("INSERT OR REPLACE INTO BookList VALUES (?,?,?,?,?,?)", Book)
    connection.commit()

def AddLoanEntry (connection: sqlite3.Connection, cursor: sqlite3.Cursor,Client: list):
    """Dodaje wpis do tabeli wypożyczonych książek.
    
    Obecnie możliwe dodanie tylko jednej książki na klienta.
    Zmniejsza stan kopii w tabeli `BookList`.

    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param Client: Dane Klientów
    :type Client: [Imię, Nazwisko, ID karty bibliotecznej, Tytuł wypożyczony]

    """
    Selection = Select(connection,cursor,"BookList","Title",Client[3])
    select = [x[5] for x in Selection]
    if select[0] < 1:
        print ("Cannot loan, not enough copies")
        return
    cursor.execute("INSERT INTO Clients VALUES (?,?,?,?)", Client)
    UpdateCopies(connection,cursor,Client[3],select[0] - 1)
    connection.commit()

def UpdateCopies (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Title, Value):
    """Aktualizuje stan kopii dla zadanej książki, zmieniająć stan kopii na podaną wartość.
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param Title: Tytuł książki
    :type Title: str
    :param Value: Nowa wartość kopii
    :type Value: int

    """
    cursor.execute("UPDATE BookList SET Copies = ? WHERE Title = ? ",(Value, Title))
    connection.commit()

def PrintTable (connection: sqlite3.Connection, cursor: sqlite3.Cursor, tableName):
    """Wyświetla zadaną tabelę.
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param tableName: Nazwa tabeli
    :type tableName: str

    """
    table = cursor.execute(f"SELECT * FROM {tableName}")
    Print(table)
    connection.commit()

def ClearTable (connection: sqlite3.Connection, cursor: sqlite3.Cursor, tableName):
    """Czyści wszystkie dane z zadanej tabeli
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param tableName: Nazwa tabeli
    :type tableName: str
    
    """
    cursor.execute(f"DELETE FROM {tableName}")
    connection.commit()

def ExportAsCSV (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    """Eksportuje dane z tabeli do pliku .csv, format pliku jest następujący
    1. wiersz - dane danej tabeli (nazwy kolumn)
    2. reszta wierszy - dane z wnętrza tabeli
    
    Funkcja ekportuje dane do dwóch plików .csv nazwanych `Book` oraz `Clients`
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    
    """

    Names = [x[0] for x in cursor.execute('select * from BookList').description]
    with open ("Books.csv", "w", newline="") as f: 
        w = csv.writer(f)
        rows = cursor.execute("SELECT * FROM BookList")
        w.writerow(Names)
        w.writerows(rows)
    Names = [x[0] for x in cursor.execute('select * from Clients').description]
    with open ("Clients.csv", "w", newline="") as f: 
        w = csv.writer(f)
        rows = cursor.execute("SELECT * FROM Clients")
        w.writerow(Names)
        w.writerows(rows)

def SortAndPrint (connection: sqlite3.Connection, cursor: sqlite3.Cursor, tableName, SortBy, ASC):
    """Sortuje wedle zadanych danych i wyświetla używając **Print ()**
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param tableName: Nazwa tabeli
    :type tableName: str
    :param SortBy: wedle jakiej kolumny sortować
    :type SortBy: str
    :param ASC: rosnąco lub malejąco
    :type ASC: str 'ASC' lub 'DSC'.
    
    """
    Print(cursor.execute(f"SELECT * FROM {tableName} ORDER BY {SortBy} {ASC}"))
    connection.commit()

def Select (connection: sqlite3.Connection, cursor: sqlite3.Cursor, tableName, selectionType, selection):
    """Przeszukuje tabelę
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor
    :param tableName: Nazwa tabeli
    :type tableName: str
    :param selectionType: Nazwa wybranej kolumny
    :type selectionType: str
    :param selection: wartość szukana
    :type selection: str
    
    :return: Znalezione wiersze
    
    """
    selected = cursor.execute(f"SELECT * FROM {tableName} WHERE {selectionType} = '{selection}'")
    connection.commit()
    return selected

def Print (selection: sqlite3.Cursor.execute):
    """Wyświetla dane tabeli.
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor

    """
    for row in selection:
        for x in zip(selection.description, row):
            print(f"{x[0][0]}: {x[1]}")
        print()

def DatabaseMode (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    """Obsługuje dialog akcji klienta.
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor

    """
    while True:    
        match input ("Welcome to database mode.\nPossible actions are:\n1. Print Table\n2. Update amount of copies\n3. Manage entries\n4.[DEBUG] Clear Table\n5. Return\n"):
            case "1":
                Table = SelectTable()
                PrintTable(connection, cursor, Table)
            case "2":
                Title = input("Title to update: ")
                Amount = input("New amount of copies: ")
                while not Amount.isdigit():
                    Amount = input ("Numeric value\nNew amount of copies: ")
                UpdateCopies(connection,cursor,Title, Amount)
            case "3":
                ManagmentMode(connection,cursor)

            case "4":
                print("F\n")
                ClearTable(connection,cursor, "BookList")
            case "5":
                break

def ManagmentMode (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    """Obsługuje dialog dotyczący zarządzania danymi w lokalnej bazie danych.
    
    :param connection: Połączenie z bazą danych sqlite3
    :type connection: sqlite3.Connection
    :param cursor: Kursor do bazy danych
    :type cursor: sqlite3.Cursor

    """
    while True:
        print()
        match input("Managing entries\n1. Delete entry\n2. Add entry\n3. Select entries (view only)\n4. return\n"):
            case "1":
                Table = SelectTable()

                Title = input("Title to remove: ")
                DeleteEntry (connection, cursor,Title,Table)
            case "2":
                Table = SelectTable()
                if Table == "BookList":
                    data = AppHandlers.BookHandler()
                    AddBook(connection,cursor,data)

                if Table == "Clients":
                    data = AppHandlers.ClientHandler()
                    AddLoanEntry(connection,cursor,data)

            case "3":
                Table = SelectTable()
                selectionType = SelectSelectionType()
                Selection = input("Selection value: ")
                Print(Select(connection,cursor,Table,selectionType,Selection))
            case "4": 
                break
                

def SelectSelectionType ():
    """Obsługa wyboru kolumny.
    
    :return: Nazwa kolumny
    """
    
    print()
    match input("1. Title\n2. Surname\n3. Cancel\n"):
        case "1":
            return "Title"
        case "2":
            return "Surname"
        case "3":
            return           

def SelectTable ():
    """Obsługa wyboru tabeli.
    
    :return: Nazwa tabeli
    """
    print()
    match input("1. List of Books\n2. List of loaners\n3. Cancel\n"):
        case "1":
            return "BookList"
        case "2":
            return "Clients"
        case "3":
            return
