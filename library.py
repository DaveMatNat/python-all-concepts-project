import os

# CONSTANTS
DEFAULT_LOCATION = "wizard_books.txt"

# Book class
class Book:
    """Represents a single book with a title and an author."""
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f'"{self.title}" - {self.author}'
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author

# Library class
class Library:
    """Manages the catalog of books."""
    def __init__(self, file_path):
        self.default = DEFAULT_LOCATION
        self.file_path = file_path
        self.books = self.import_books(file_path)

    def import_books(self, filename):
        """
        Reads a book file and loads the data into a list.
        If the file isn't there, let's try the default file.
        """
        books = [] 
        # if file doesn't exist, return empty list
        if not os.path.isfile(self.default):
            print("Oops! Default Book file is missing, please make sure it is available in the directory for the Program to work properly!".title())
            return books
        try:
            with open(filename, "r") as file:
                for line in file:
                    title, author = line.strip().split(" - ")
                    books.append(Book(title.strip('"'), author))
        except FileNotFoundError:
            # file not found --> print messege below and call this function but using default_file as parameter instead
            print(f"ERROR: Book file [{filename}] not found! Defaulting to '{os.path.basename(self.default)}'")
            return self.import_books(self.default)
        return books

    def export_books(self, sorted_books, filename):
        """Exports sorted book data to a file."""
        with open(filename, "w") as file:
            for title, author in sorted_books:
                file.write(f'"{title}" - {author}\n')

    def sort_books(self, criteria):
        if criteria == "title":
            return sorted(self.books, key=lambda book: book.get_title())
        elif criteria == "author":
            return sorted(self.books, key=lambda book: book.get_author().split()[-1])
        else:
            return self.books

    def search_books(self, books, criteria):
        while True:
            print("[SEARCH MENU] Enter your search keyphrase or type 'back' to return")
            ip = input("> ").strip().lower()
            # go back to main menu
            if ip == "back":
                break

            # initialize an empty list to store search results
            results = []
            # search algorithm: append results from book_catalog according to criteria and if the keyword exists
            for book in books:
                if (criteria == "title" and ip in book.get_title().lower()) or \
                (criteria == "author" and ip in book.get_author().lower()) or \
                (criteria == "either" and (ip in book.get_title().lower() or ip in book.get_author().lower())):
                    results.append(book)
            # if list is not empty, print the formated results
            if results:
                print(f"=== MATCHES FOR [{ip}] ===")
                for book in results:
                    print(f'"{book.get_title()}" - {book.get_author()}')
                print("=====================================")
            else:
            # list is empty, no matches found
                print(f"===== NO MATCHES FOUND FOR THE SEARCH [{ip}] =====")
    def get_books(self):
        return self.books


# WizardLibrarianInterface class
class WizardLibrarianInterface:
    """Handles the user interface and main app logic."""
    def __init__(self, file_path):
        self.library = Library(file_path)
        self.file_name = os.path.basename(file_path).split(".")[0]

    def main_menu(self):
        """
        Main menu of the Wizard Librarian app.
        The main menu displays the following options to the user:

            sort: calls the sort_menu() function to sort the books
            search: calls the search_menu() function to search the books
            exit: exits the entire app with a goodbye message
        """
        while True:
            print("\n[MAIN MENU] Welcome to the Wizard Library! What would you like to do? [sort, search, exit]")
            ip = input("> ").strip().lower()
            
            # Sort --> sort_menu()
            if ip == "sort":
                self.sort_menu()

            # Search --> search_menu() --> search_books()
            elif ip == "search":
                self.search_menu()

            # Exit --> break loop --> *exits* main_menu()
            elif ip == "exit":
                print("Thank you for visiting the Wizard Library! Hope to see you again :D")
                break
    def sort_menu(self):
        """
        The sort menu displays the following options to the user:

            title: sorts the books by title
            author: sorts the books by author's last name
            back: returns to the main menu
        """
        while True:
            print("[SORT MENU] How would you like to sort the catalog? [title, author, back]")
            ip = input("> ").strip().lower()

            # If ip is title, sort the book by the first index (0) which corresponds to the book's title
            if ip == "title":
                sorted_books = self.library.sort_books(ip)
                self.library.export_books([(book.get_title(), book.get_author()) for book in sorted_books], f"{self.file_name}_TITLE.txt")
                print(f"*** Books were sorted by title and exported to {self.file_name}_TITLE.txt ***")
                break
            # If ip is author, sort the book by last name of the second index (1) which corresponds to the book's author
            elif ip == "author":
                sorted_books = self.library.sort_books(ip)
                self.library.export_books([(book.get_title(), book.get_author()) for book in sorted_books], f"{self.file_name}_AUTHOR.txt")
                print(f"*** Books were sorted by author and exported to {self.file_name}_AUTHOR.txt ***")
                break
            # Exit loop --> *exits* sort_menu() --> main_menu()
            elif ip == "back":
                break

    def search_menu(self):
        """
        Asks the user what they would like to search by and calls search_books() with the
        specified criteria. If user enters 'back', returns to main menu by exiting this 
        function through breaking the loop.

        Inputs:
            title: book title
            author: book author's Last Name
            either: both title and author
            back: return to main menu
        """
        while True:
            print("[SEARCH MENU] How would you like to search by? [title, author, either, back]")
            ip = input("> ").strip().lower()

            if ip == "title":
                books = self.library.import_books(f"{self.file_name}_TITLE.txt")
                self.library.search_books(books,"title")
            elif ip == "author":
                books = self.library.import_books(f"{self.file_name}_AUTHOR.txt")
                self.library.search_books(books,"author")
            elif ip == "either":
                books = self.library.import_books(self.library.file_path)
                self.library.search_books(books,"either")
            elif ip == "back":
                break

# Run the application
if __name__ == "__main__":
    app = WizardLibrarianInterface(DEFAULT_LOCATION)
    app.main_menu()