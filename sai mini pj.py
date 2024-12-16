import pandas as pd
from datetime import datetime

class LibraryManagement:
    def __init__(self):
        self.books = pd.DataFrame(columns=['ID', 'Title', 'Author', 'Genre', 'Copies'])
        self.members = pd.DataFrame(columns=['ID', 'Name', 'Email'])
        self.transactions = pd.DataFrame(columns=['TransactionID', 'MemberID', 'BookID', 'IssueDate', 'ReturnDate'])
        self.book_id_counter = 1
        self.member_id_counter = 1
        self.transaction_id_counter = 1

    def add_book(self, title, author, genre, copies):
        self.books = pd.concat([
            self.books,
            pd.DataFrame({
                'ID': [self.book_id_counter],
                'Title': [title],
                'Author': [author],
                'Genre': [genre],
                'Copies': [copies]
            })
        ], ignore_index=True)
        print(f"Book '{title}' added successfully with ID {self.book_id_counter}.")
        self.book_id_counter += 1

    def add_member(self, name, email):
        if email in self.members['Email'].values:
            print("Error: A member with this email already exists.")
            return
        self.members = pd.concat([
            self.members,
            pd.DataFrame({
                'ID': [self.member_id_counter],
                'Name': [name],
                'Email': [email]
            })
        ], ignore_index=True)
        print(f"Member '{name}' added successfully with ID {self.member_id_counter}.")
        self.member_id_counter += 1

    def issue_book(self, member_id, book_id):
        book = self.books.loc[self.books['ID'] == book_id]
        if book.empty or book.iloc[0]['Copies'] <= 0:
            print("Error: Book is not available.")
            return

        self.transactions = pd.concat([
            self.transactions,
            pd.DataFrame({
                'TransactionID': [self.transaction_id_counter],
                'MemberID': [member_id],
                'BookID': [book_id],
                'IssueDate': [datetime.now().strftime('%Y-%m-%d')],
                'ReturnDate': [None]
            })
        ], ignore_index=True)

        self.books.loc[self.books['ID'] == book_id, 'Copies'] -= 1
        print(f"Book ID {book_id} issued to Member ID {member_id}.")
        self.transaction_id_counter += 1

    def return_book(self, transaction_id):
        transaction = self.transactions.loc[self.transactions['TransactionID'] == transaction_id]
        if transaction.empty or pd.notna(transaction.iloc[0]['ReturnDate']):
            print("Error: Invalid transaction ID or book already returned.")
            return

        book_id = transaction.iloc[0]['BookID']
        self.transactions.loc[self.transactions['TransactionID'] == transaction_id, 'ReturnDate'] = datetime.now().strftime('%Y-%m-%d')
        self.books.loc[self.books['ID'] == book_id, 'Copies'] += 1
        print(f"Transaction ID {transaction_id}: Book returned successfully.")

    def display_books(self):
        if self.books.empty:
            print("No books available in the library.")
        else:
            print("\nBooks in Library:")
            print(self.books.to_string(index=False))


def main():
    library = LibraryManagement()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            genre = input("Enter genre: ")
            copies = int(input("Enter number of copies: "))
            library.add_book(title, author, genre, copies)
        elif choice == '2':
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            library.add_member(name, email)
        elif choice == '3':
            member_id = int(input("Enter member ID: "))
            book_id = int(input("Enter book ID: "))
            library.issue_book(member_id, book_id)
        elif choice == '4':
            transaction_id = int(input("Enter transaction ID: "))
            library.return_book(transaction_id)
        elif choice == '5':
            library.display_books()
        elif choice == '6':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
