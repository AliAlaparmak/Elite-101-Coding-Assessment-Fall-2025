from datetime import datetime, timedelta
import json
import time

# -------- Level 5 --------
# TODO: Convert your data into a Book class with methods like checkout() and return_book()
# TODO: Add a simple menu that allows the user to choose different options like view, search, checkout, return, etc.

#                 README ADDITIONAL NOTES
#The code loads all the data from the json file into a list of Book objects when the program starts, and saves any changes back to the json file when the program exits.
#This way, any checkouts, returns, or new books added will persist between program runs.
#I really enjoyed working on this project and actually learned a lot about working on bigger programs with multiple features that can interfere with each other.
#One thing I would like to continue adding on is a UI as well as a log in system where indivdiual users can log in and have their own checkout history.


#Converted my library book dictionary into a json file to allow me to save and laod data without losing it when the program stops running.
#Used https://docs.python.org/3/library/json.html to help with json file handling and Data Saving and loading.
class Book:
    def __init__(self, id, title, author, genre, available, due_date, checkouts):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available
        self.due_date = due_date
        self.checkouts = checkouts

   #Operation 3
    def checkout(self):
        if self.available:
            self.available = False
            #https://www.w3schools.com/python/python_datetime.asp Used documenation, and help from Ai for help with handling dates.
            self.due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            self.checkouts += 1
            print(f"Book '{self.title}' checked out complete. Due date is {self.due_date}.")
            time.sleep(0.5); print()
            return True
        print(f"Book '{self.title}' is unavaliable until {self.due_date}.")
        time.sleep(0.5); print()
        return False
    
    #Operation 4
    def return_book(self):
        if not self.available:
            self.available = True
            self.due_date = None
            print("Book returned.")
            time.sleep(0.5); print()
            return True
        print("This book was not checked out.")
        time.sleep(0.5); print()
        return False


def load_books():
    with open('library_books.json', 'r') as file:
        data = json.load(file)

    books_catalog = []
    for book in data:
        Cbook = Book(
            id=book['id'],
            title=book['title'],
            author=book['author'],
            genre=book['genre'],
            available=book['available'],
            due_date=book['due_date'],
            checkouts=book['checkouts']
        )
        books_catalog.append(Cbook)
    return books_catalog 


#Operation 7
def catalog_update(books_catalog):
    book_name = input("Enter the title of the book to add: ")
    author_name = input("Enter the author of the book: ")
    genre_name = input("Enter the genre of the book: ")
    
    new_book = Book(
        #created unique Book ID's for each new book by adding 1 to the length of the catalog.
        id="B" + str(len(books_catalog) + 1),
        title=book_name,
        author=author_name,
        genre=genre_name,
        available=True,
        due_date=None,
        checkouts=0
    )
    books_catalog.append(new_book)
    print(f"{book_name} by {author_name} added to the catalog.")
    time.sleep(0.5); print()


#Operation 8
def save_books(books_catalog):
    data = []
    for book in books_catalog:
        data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'available': book.available,
            'due_date': book.due_date,
            'checkouts': book.checkouts
        })

    with open('library_books.json', 'w') as file:
        json.dump(data, file, indent=4)


#Operation 6
def top_checked_out_books(books_catalog):
    #https://www.w3schools.com/python/ref_func_sorted.asp   Had a lot of help from code snippets as well as AI on how to use the sorted function with lambda to sort my books by checkouts.
    sorted_books = sorted(books_catalog, key=lambda b: b.checkouts, reverse=True)
    top_three = sorted_books[:3]
    print("\nTop 3 Most Checked-Out Books:")
    time.sleep(0.5); print()
    for i, book in enumerate(top_three, start=1):
        print(f"{i}. {book.title} - {book.checkouts} checkouts")
        time.sleep(0.5); print()


#Operation 1
def view_available_books(books_catalog):
    print("\nAvailable Books:")
    time.sleep(0.5)
    for book in books_catalog:
        if book.available:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")
            time.sleep(0.5)


#Operation 2
def search_books(books_catalog):
    Search_category = input("Search by Title, Author, or Genre? (T/A/G): ").strip().lower()
    if Search_category not in ['t', 'a', 'g']:
        print("Invalid category. Please enter T, A, or G.")
        time.sleep(0.5); print()
        return
    else:
        Search_bar = input("Enter your search term: ").strip().lower()
        print("\nSearch Results:\n")
        time.sleep(0.5); print()

    for book in books_catalog:
        if Search_category == 't':
            field = book.title.lower()
        elif Search_category == 'a':
            field = book.author.lower()
        else:
            field = book.genre.lower()

        if Search_bar in field and book.available:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")
            time.sleep(0.5); print()


#Operation 5
def list_overdue_books(books_catalog):
    current_date = datetime.now()
    overdue_list = []
    print("\nOverdue Books:")
    time.sleep(0.5); print()
    for book in books_catalog:
        if book.due_date is not None:
            #also used help from https://www.w3schools.com/python/python_datetime.asp to help with date comparisons.
            due_date = datetime.strptime(book.due_date, "%Y-%m-%d")
            if due_date < current_date:
                overdue_list.append(book.title)

    if not overdue_list:
        print("No overdue books.")
        time.sleep(0.5); print()
        return
    
    for title in overdue_list:
        print(title)
        time.sleep(0.5); print()


# main loop
def main():
    
    books_catalog = load_books()
    while True:
        time.sleep(0.5); print()
        User_inp = input(" Welcome to our Digital Library System. Please enter numbers 1-8 to select your desired operation: \n1.) View Available Books \n2.) Search Books \n3.) Checkout Book \n4.) Return Book \n5.) List Overdue Books \n6.) View Top 3 Most Checked-out Books\n7.) Add a book to catalog\n8.) Exit\nUser: ")

        if User_inp == '1':
            view_available_books(books_catalog)

        elif User_inp == '2':
            search_books(books_catalog)

        elif User_inp == '3':
            name = input("Enter the title of the book you want to checkout: ")
            for book in books_catalog:
                if book.title.lower() == name.lower():
                    book.checkout()

        elif User_inp == '4':
            name = input("Enter the title of the book you want to return: ")
            for book in books_catalog:
                if book.title.lower() == name.lower():
                    book.return_book()

        elif User_inp == '5':
            list_overdue_books(books_catalog)

        elif User_inp == '6':
            top_checked_out_books(books_catalog)

        elif User_inp == '7':
            catalog_update(books_catalog)

        elif User_inp == '8':
            save_books(books_catalog)
            print("Exiting the system. Goodbye!")
            time.sleep(0.5); print()
            break

        else:
            print("Invalid input. Please enter a number between 1 and 8.")
            time.sleep(0.5); print()


if __name__ == "__main__":
    main()
