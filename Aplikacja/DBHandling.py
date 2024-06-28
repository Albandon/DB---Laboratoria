import csv
import sqlite3

def CSVtoDB (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    z = open ("file.csv",newline='')
    reader = csv.reader(z, delimiter=',')
    for row in reader:
        cursor.execute("INSERT OR REPLACE INTO BookList VALUES (?,?,?,?,?,?,?)", row)
    connection.commit()

def DeleteBook (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Title):
    cursor.execute("DELETE FROM BookList WHERE Title = (?)", (Title,))
    connection.commit()

def AddBook (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Book: list):
    cursor.execute("INSERT OR REPLACE INTO BookList VALUES (?,?,?,?,?,?,?)", Book)
    connection.commit()

def UpdateCopies (connection: sqlite3.Connection, cursor: sqlite3.Cursor, Title, Value):
    cursor.execute("UPDATE BookList SET Copies = ? WHERE Title = ? ",(Value, Title))
    connection.commit()

def PrintTable (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    for row in cursor.execute("SELECT * FROM BookList"):
        print(row)
    connection.commit()

def ClearDB (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    cursor.execute("DELETE FROM BookList")
    connection.commit

def ExportAsCSV (connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    Names = [des[0] for des in cursor.description]
    with open ("temp.csv", "w", newline="") as f: 
        w = csv.writer(f)
        rows = cursor.execute("SELECT * FROM BookList")
        w.writerow(Names)
        w.writerows(rows)