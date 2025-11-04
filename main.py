from datetime import datetime, timedelta
import json
import time

# -------- Level 5 --------
# TODO: Convert your data into a Book class with methods like checkout() and return_book()
# TODO: Add a simple menu that allows the user to choose different options like view, search, checkout, return, etc.

# -------- Optional Advanced Features --------
# You can implement these to move into Tier 4:
# - Add a new book (via input) to the catalog
# - Sort and display the top 3 most checked-out books
# - Partial title/author search
# - Save/load catalog to file (CSV or JSON)
# - Anything else you want to build on top of the system!


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

    def checkout(self):
        if self.available:
            self.available = False
            #https://docs.python.org/3/library/datetime.html. Used Datimetme documenatation to help with moost of the date functionality. Used help from ChatGPT also.
            self.due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            self.checkouts += 1
            print(f"Book '{self.title}' checked out complete. Due date is {self.due_date}.")
            return True
        print(f"Book '{self.title}' is unavaliable until {self.due_date}.")
        return False

    def return_book(self):
        if not self.available:
            self.available = True
            self.due_date = None
            print("Book returned.")
            return True
        print("This book was not checked out.")
        return False

def load_books():
    with open('library_books.json', 'r') as file:
        data = json.load(file)
    #Active memory list of book objects
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

def catalog_update(books_catalog):
    book_name = input("Enter the title of the book to add: ")
    author_name = input("Enter the author of the book: ")
    genre_name = input("Enter the genre of the book: ")
    
    new_book = Book(
        #using the length of the current catalog than adding one to create a unique ID for every book. 
        id=len(books_catalog) + 1,
        title=book_name,
        author=author_name,
        genre=genre_name,
        available=True,
        due_date=None,
        checkouts=0
    )
    books_catalog.append(new_book)
    print(f"{book_name} by {author_name} added to the catalog.")
        
#neccesary for saving the books after code is stopped or restarted.
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
   

def top_checked_out_books(books_catalog):
    #https://www.w3schools.com/python/ref_func_sorted.asp to help with sorting, as well as ChatGPT to help w Planning logic.
    sorted_books = sorted(books_catalog, key=lambda b: b.checkouts, reverse=True)
    top_three = sorted_books[:3]
    print("\nTop 3 Most Checked-Out Books:")
    for i, book in enumerate(top_three, start=1):
        print(f"{i}. {book.title} - {book.checkouts} checkouts")

def view_available_books(books_catalog):
    print("\nAvailable Books:")
    for book in books_catalog:
        if book.available:
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")

def search_books(books_catalog):
    #Using three different categories for searching.
    Search_category = input("Search by Title, Author, or Genre? (T/A/G): ").strip().lower()
    if Search_category not in ['t', 'a', 'g']:
        print("Invalid category. Please enter T, A, or G.")
    else:
        Search_bar = input("Enter your search term: ").strip().lower()
        print("\nSearch Results:")

    for book in books_catalog:
        # choose which field to check
        if Search_category == 't':
            field = book.title.lower()
        elif Search_category == 'a':
            field = book.author.lower()
        else:
            field = book.genre.lower()
    
    if Search_bar in field and book.available:
        print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}")

# main loop for user interaction
def main():
    
    books_catalog = load_books()
    while True:
        User_inp = input(" Welcome to our Digital Library System. Please enter numbers 1-8 to select your desired operation: \n1.) View Available Books \n2.) Search Books \n3.) Checkout Book \n4.) Return Book \n5.) List Overdue Books \n6.)View Top 3 Most Checked-out Books\n Add a book to catalog\n8.) Exit\nUser: ")
        if User_inp == '1':
            view_available_books(books_catalog)
        elif User_inp == '2':
            search_books(books_catalog)
        elif User_inp == '3':
            pass
        elif User_inp == '4':
            pass
        elif User_inp == '5':
            pass
        elif User_inp == '6':
            top_checked_out_books(books_catalog)
        elif User_inp == '7':
            catalog_update(books_catalog)
        elif User_inp == '8':
            save_books()
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 8.")



if __name__ == "__main__":
    main()
    pass
