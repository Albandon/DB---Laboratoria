import csv
import validators

def SaveAsCsv (a: dict):
    with open ("file.csv", "w", newline="") as f: 
        w = csv.DictWriter(f, a[0].keys())
        # w.writeheader()
        for key, items in a.items():
            w.writerow(items)

def BookHandler ():
    while True:
        Name = input("\tName: ")
        if Name.isalpha():
            break
        print("Name must contain letters only")
    while True:
        Surname = input("\tSurname: ")
        if Surname.isalpha():
            break
        print("Surname must contain letters only")
    # title may contain different characters and numbers so no validation    
    Title = input("\tTitle: ")

    # while True:
    #     Price = input("\tPrice: ")
    #     if Price.isdigit():
    #         if len(Price) > 4: print ("Chyba w rublach koleszko")
    #         break
    #     print("Price must be a number")

    while True:
        Page = input("\tNumber of pages: ")
        if Page.isdigit():
            break
        print("number!!")
    
    while True:
        CoO = input("\tCountry of Origin (eg. POL): ")
        if validators.country_code(CoO, iso_format = "alpha3"):
            break
        print("Name of the country in 3-letter format")
        
    while True:
        Copies = input("\tCopies of the Book: ")
        if Copies.isdigit():
            break
        print ("number!!")
    return [Name, Surname, Title, Page, CoO, Copies]

def ClientHandler ():
    while True:
        Name = input("\tName: ")
        if Name.isalpha():
            break
        print("Name must contain letters only")
    while True:
        Surname = input("\tSurname: ")
        if Surname.isalpha():
            break
        print("Surname must contain letters only")
    while True:
        LibraryID = input("\tLibrary Card ID (6-digit): ")
        if LibraryID.isdigit() and len(LibraryID) == 6:
            break
        print("Library card id needs to numeric and 6-digit long")
    LoanedTitle = input("\tTitle Loaned: ")
    return [Name,Surname,LibraryID,LoanedTitle]



def AddBook ():
    # Get and Validate data

    Input = BookHandler()
    # Allow user to double-check
    data = {"Name": Input[0],
        "Surname": Input[1],
        "Title": Input[2],
        "Page": Input[4],
        "CoO": Input[5],
        "Copies": Input[6]}
    print (data)
    if not input("Correct[y]") == "y":
        return
    return data
    