import mysql.connector

def add_product(name, category,quantity, price):
    
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()

    
    cursor.execute("INSERT INTO products (name, category, price, quantity) VALUES (%s, %s, %s, %s)", 
                   (name, category, price, quantity))
    connection.commit()
    connection.close()
    print("Product added successfully.")

def edit_product(product_id, name=None, category=None, quantity=None, price=None):
    
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    
    updates = []
    values = []
    
    if name:
        updates.append("name = %s")
        values.append(name)
    if category:
        updates.append("category = %s")
        values.append(category)
    if price is not None:
        updates.append("price = %s")
        values.append(price)
    if quantity is not None:
        updates.append("quantity = %s")
        values.append(quantity)
    
    values.append(product_id)
    query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
    cursor.execute(query, values)
    connection.commit()
    connection.close()
    print("Product updated successfully.")

def delete_product(product_id):

    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()

    
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    connection.commit()
    connection.close()
    print("Product deleted successfully.")

def view_products():
    try:
        connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        connection.close()
        
        for prod in products:
            print (prod)
        return products
    
    except mysql.connector.Error as err:
        print("Database Error:", err)
        return []

if __name__ == "__main__":
    choice = input("Do you want to add, edit, delete, or view products? (a/e/d/v): ")
    if choice == 'a':
        name = input("Enter product name: ")
        category = input("Enter category: ")
        price = float(input("Enter price: "))
        quantity = int(input("Enter quantity: "))
        add_product(name, category, price, quantity)
    elif choice == 'e':
        product_id = int(input("Enter product ID: "))
        name = input("Enter new name (leave blank to keep unchanged): ") or None
        category = input("Enter new category (leave blank to keep unchanged): ") or None
        price = input("Enter new price (leave blank to keep unchanged): ")
        price = float(price) if price else None
        quantity = input("Enter new quantity (leave blank to keep unchanged): ")
        quantity = int(quantity) if quantity else None
        edit_product(product_id, name, category, price, quantity)
    elif choice == 'd':
        product_id = int(input("Enter product ID to delete: "))
        delete_product(product_id)
    elif choice == 'v':
        view_products()
