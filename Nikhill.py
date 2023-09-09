import pymysql

# Database connection variables
db_host = 'localhost'
db_user = 'root'
db_password = 'Rajdevy25!@'
db_name = 'restaurant'

def authenticate_and_connect(username, password):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = conn.cursor()
    
    query = "SELECT role FROM Users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    
    if cursor.rowcount == 1:
        role = cursor.fetchone()[0]
        print(f"Welcome, {role}!")
        
        if role == 'Staff':
            take_order(cursor)
            
        if role == 'Manager':
            manage_menu(cursor)
            handle_billing(cursor)
        
        conn.commit()
        return conn

    else:
        print("Authentication failed.")
        return None

def take_order(cursor):
    query = "SELECT item_id, item_name, price FROM Menu"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print("Available items:")
    for row in rows:
        print(f"ID: {row[0]}, Item Name: {row[1]}, Price: {row[2]}")
        
    item_id = input("Enter the item ID you want to order: ")
    quantity = input("Enter the quantity: ")
    query = "INSERT INTO Orders (item_id, quantity) VALUES (%s, %s)"
    cursor.execute(query, (item_id, quantity))
    print(f"Order placed for item {item_id} with quantity {quantity}.")

def manage_menu(cursor):
    print("1. Add Item")
    print("2. Delete Item")
    choice = input("Choose an option: ")
    
    if choice == '1':
        item_name = input("Enter item name: ")
        price = input("Enter price: ")
        query = "INSERT INTO Menu (item_name, price) VALUES (%s, %s)"
        cursor.execute(query, (item_name, price))
        print(f"Item {item_name} added.")

    elif choice == '2':
        item_id = input("Enter the item ID to delete: ")
        query = "DELETE FROM Menu WHERE item_id = %s"
        cursor.execute(query, (item_id,))
        print(f"Item {item_id} deleted.")

def handle_billing(cursor):
    query = '''SELECT Orders.order_id, Menu.item_name, Menu.price, Orders.quantity,
    (Menu.price * Orders.quantity) as Total_Price
    FROM Orders JOIN Menu ON Orders.item_id = Menu.item_id'''
    
    cursor.execute(query)
    rows = cursor.fetchall()

    print("Order ID | Item Name | Price | Quantity | Total Price")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

# Example usage
conn = authenticate_and_connect('Manager', '11111')
if conn:
    print("Connected to the database.")
    conn.close()
else:
    print("Not connected.")
