import pymysql

# **Step 0**: Database connection variables
db_host = 'localhost'
db_user = 'root'
db_password = 'Rajdevy25!@'
db_name = 'restaurant'

# **Step 1**: User Authentication and Menu
def authenticate_and_connect(username, password):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = conn.cursor()
    
    query = "SELECT role FROM Users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    
    if cursor.rowcount == 1:
        role = cursor.fetchone()[0]
        print(f"Welcome, {role}!")
        
        while True:
            if role == 'Staff':
                print("\n1. Take Order")
                print("2. Exit")
                choice = input("Enter your choice: ")
                
                if choice == '1':
                    take_order(cursor)
                elif choice == '2':
                    break
                else:
                    print("Invalid choice.")
                    
            elif role == 'Manager':
                print("\n1. Take Order")
                print("2. Manage Menu")
                print("3. Handle Billing")
                print("4. Exit")
                choice = input("Enter your choice: ")

                if choice == '1':
                    take_order(cursor)
                elif choice == '2':
                    manage_menu(cursor)
                elif choice == '3':
                    handle_billing(cursor)
                elif choice == '4':
                    break
                else:
                    print("Invalid choice.")
                    
            conn.commit()
        
        conn.close()
        return conn
    else:
        print("Authentication failed.")
        return None

# **Step 2**: Taking Orders with Validations
def take_order(cursor):
    query = "SELECT item_id, item_name, price FROM Menu"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print("Available items:")
    for row in rows:
        print(f"ID: {row[0]}, Item Name: {row[1]}, Price: {row[2]}")
        
    item_id = input("Enter the item ID you want to order: ")
    quantity = int(input("Enter the quantity: "))
    
    if 1 <= quantity <= 5:
        query = "INSERT INTO Orders (item_id, quantity) VALUES (%s, %s)"
        cursor.execute(query, (item_id, quantity))
        print(f"Order placed for item {item_id} with quantity {quantity}.")
    else:
        print("Order quantity should not exceed 5.")

# **Step 3**: Managing Menu with Validations
def manage_menu(cursor):
    print("1. Add Item")
    print("2. Delete Item")
    choice = input("Choose an option: ")
    
    if choice == '1':
        item_name = input("Enter item name: ")
        
        if 1 <= len(item_name) <= 20:
            price = int(input("Enter price: "))
            
            if 100 <= price <= 1000:
                query = "INSERT INTO Menu (item_name, price) VALUES (%s, %s)"
                cursor.execute(query, (item_name, price))
                print(f"Item {item_name} added.")
            else:
                print("Price should be between 100 and 1000.")
        else:
            print("Item name should be between 1 and 20 characters.")
    
    elif choice == '2':
        item_id = input("Enter the item ID to delete: ")
        query = "DELETE FROM Menu WHERE item_id = %s"
        cursor.execute(query, (item_id,))
        print(f"Item {item_id} deleted.")

# Handling Billing
def handle_billing(cursor):
    query = '''SELECT Orders.order_id, Menu.item_name, Menu.price, Orders.quantity,
    (Menu.price * Orders.quantity) as Total_Price
    FROM Orders JOIN Menu ON Orders.item_id = Menu.item_id'''
    
    cursor.execute(query)
    rows = cursor.fetchall()

    print("Order ID | Item Name | Price | Quantity | Total Price")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

# **Main Program**
if __name__ == '__main__':
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    conn = authenticate_and_connect(username, password)
    
    if not conn:
        print("Authentication failed.")
