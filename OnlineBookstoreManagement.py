import mysql.connector
from datetime import date

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password="password",  # Replace with your MySQL password
    database="OnlineBookstore"
)

cursor = conn.cursor()

# Function to add a new book
def add_book(title, author, genre, price, stock):
    cursor.execute("""
        INSERT INTO Books (Title, Author, Genre, Price, Stock)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, author, genre, price, stock))
    conn.commit()

# Function to retrieve books by author
def get_books_by_author(author):
    cursor.execute("SELECT * FROM Books WHERE Author = %s", (author,))
    return cursor.fetchall()

# Function to create a new order
def create_order(customer_id, book_id, quantity):
    # Get the price of the book
    cursor.execute("SELECT Price FROM Books WHERE BookID = %s", (book_id,))
    price = cursor.fetchone()[0]
    
    # Calculate total amount
    total_amount = price * quantity
    
    # Create a new order
    cursor.execute("""
        INSERT INTO Orders (CustomerID, OrderDate, TotalAmount)
        VALUES (%s, %s, %s)
    """, (customer_id, date.today(), total_amount))
    order_id = cursor.lastrowid
    
    # Insert into order details
    cursor.execute("""
        INSERT INTO OrderDetails (OrderID, BookID, Quantity, Price)
        VALUES (%s, %s, %s, %s)
    """, (order_id, book_id, quantity, price))
    
    # Update book stock
    cursor.execute("UPDATE Books SET Stock = Stock - %s WHERE BookID = %s", (quantity, book_id))
    
    conn.commit()

# Function to calculate total sales revenue
def calculate_total_revenue():
    cursor.execute("SELECT SUM(TotalAmount) FROM Orders")
    return cursor.fetchone()[0]

# Example usage
add_book('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 10.99, 50)
books_by_author = get_books_by_author('F. Scott Fitzgerald')
create_order(1, 1, 2)  # Assuming CustomerID = 1 and BookID = 1
total_revenue = calculate_total_revenue()

print("Books by F. Scott Fitzgerald:", books_by_author)
print("Total Revenue:", total_revenue)

# Close the connection
cursor.close()
conn.close()
