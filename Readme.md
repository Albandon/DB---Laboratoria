# DB using "application" made as an laboratory assigment 
Requires Python 3.12 or greater and poetry 1.8 or greater

## Installation:
to install all you need to do is:
1. Open terminal
2. Go to directory inside downloaded repository
3. execute following:
```
poetry update
poetry shell
python Aplikacja/App.py
```

### Current functionality consists of:
- adding new Entries
- exporting the entries as .csv file
- editing existing entries (db mode)
- deleting entries (db mode)
- Sorting and viewing tables (db mode)
- selecting specific data (db mode)
- clearing whole table (debug)
- Importing data form .csv
___
### To do:
- ~~extend user "interface"~~
- translate readme
- ~~add client table~~
- ~~extend the export function with additional table~~

# How to use (in progress):
Run the aplication. You are now in standard user mode from here you are able to add a book, save the changes you made, exit the app or switch to database mode.

Database mode exist purely to allow you further control over the local database (the one on your PC). From here you gain access to modify or erase all of the entered data you also can export or import database from an .csv file

Remeber to double check what you are going to do and proced with caution.

## Functions:
Most of the functions are self explanatory so I will try to explain only those which are not. Those functions are in DB mode
### Add/Delete
adds or deletes data into specified by dialog table with further specified by your input values. It's important to note that removing client from loan table will cause book to return and thus increment number of copies. Other important thing to mention is that you can't add more than one book to the client.
### Update Copies
Works only for Book table. Will change the value of Copies to the one you specified;
Check current number beforehand.
### Select Specific
Selects **all** of the data that matches your search.
For example if you select Book title from loaned table you will get all of the people who have it as loaned.
### Clearing whole
Clears whole table, as of now has no safeguard and deletes all of the book entries from the book table (planned further ability to select desired table)

### Save to CSV (standard mode)
Currently saves the data with first row containing names of the columns. Save is performed into two seperate files.

___
