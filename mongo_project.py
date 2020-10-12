import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")  # Gets the URI from the env.py file
DATABASE = "MyTestDB"
COLLECTION = "MyFirstMDB"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter Option:")
    return option

def get_record():
    print("")
    first = input("Enter first name >")  # Our searches are going to based by name
    last = input("Enter last name >")

    try: 
        doc = coll.find_one({'first': first.lower(), 'last': last.lower()})  # This variable holds a cursor object if we can find our record
    except:
        print("Error accessing the database.")

    if not doc:
        print("")
        print("Error! No results found")
    
    return doc

def add_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_colour = input("Enter hair colour > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")

    new_doc = {'first': first.lower(), 'last': last.lower(), 'dob': dob,
               'gender': gender, 'hair_colour': hair_colour, 'occupation':
               occupation, 'nationality': nationality}
    
    try:
        coll.insert_one(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")

"""
define a function called find record which gets the reults
of our get record function
"""

def find_record():
    doc = get_record()  # This is a cursor object that consists of the dictionary holding the results from the get record function
    if doc:  # if we have some results print a blank line the use a for loop to iterate through the keys and values
        print("")
        for k,v in doc.items():  # This uses the items method to step through each individual value in the dictionary
            if k != "_id":  # If the key returned is not the ID then we want to print the key
                print(k.capitalize() + ": " + v.capitalize())  # We want to capitalize the key and the value


def edit_record():
    doc = get_record()  # Store the reults of our get record function in a variable called doc
    if doc:  # Check to see if there is something in the dictionary
        update_doc = {}  # Create an empty dictionary, we will add to this as we iterate through or keys and values
        print("")
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")  # The value for the key in update_doc is equal to the input

                if update_doc[k] == "":  # if nothing has been entered, we don't want to delete the information so we set it back to v
                    update_doc[k] = v

        try:
            coll.update_one(doc, {'$set': update_doc})  # Pass in the update doc dictionaryy to update, using the set keyword
            print("")
            print("Document was updated")
        except:
            print("Error accessing the database")

def delete_record():
    doc = get_record()

    if doc:  # We iterate through to make sure we're deleting the correct document
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        print("")

        if confirmation.lower() == 'y':
            try:
                coll.delete_one(doc)
                print("Document deleted!")
            except:
                print("Document not deleted")
        else:
            print("Document not deleted!")

"""
Define the main loop which will continue to call the
menu every time we come back to it.
We store the result of our show menu function in a
variable called option.
Each option chosen calls the relevant function when entered.
Option 5 closes the connection and breaks the while loop.
Finish with an else statement that prints Invalid Option
"""
def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid Option")
        print("")

conn = mongo_connect(MONGO_URI)  # Connections taken from mongo.py file

coll = conn[DATABASE][COLLECTION]  

main_loop()  # Calls the main loop function