import csv
def SaveAsCsv (a: dict):
    with open ("file.csv", "w", newline="") as f: 
        w = csv.DictWriter(f, a[0].keys())
        # w.writeheader()
        for key, items in a.items():
            w.writerow(items)

def AddBook ():
    # Get and Validate data
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

    while True:
        Price = input("\tPrice: ")
        if Price.isdigit():
            if len(Price) > 4: print ("Chyba w rublach koleszko")
            break
        print("Price must be a number")

    while True:
        Page = input("\tNumber of pages: ")
        if Page.isdigit():
            break
        print("number!!")
    
    while True:
        CoO = input("\tCountry of Origin: ")
        if CoO.isalpha():
            break
        print("Name of the country")
        
    while True:
        Copies = input("\tCopies of the Book: ")
        if Copies.isdigit():
            break
        print ("number!!")

    # Allow user to double-check
    data = {"Name": Name,
        "Surname": Surname,
        "Title": Title,
        "Price": Price,
        "Page": Page,
        "CoO": CoO,
        "Copies": Copies}
    print (data)
    return data
    