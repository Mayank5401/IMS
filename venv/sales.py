import mysql.connector
import matplotlib.pyplot as plt

def record_sale(product_id, quantity_sold):
    
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    # Check if product exists and has enough stock
    cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        print("Error: Product not found.")
        connection.close()
        return
    
    if product[0] < quantity_sold:
        print("Error: Not enough stock available.")
        connection.close()
        return
    
    # Update product quantity
    new_quantity = product[0] - quantity_sold
    cursor.execute("UPDATE products SET quantity = %s WHERE id = %s", (new_quantity, product_id))
    
    # Record the sale
    cursor.execute("INSERT INTO sales (product_id, quantity_sold,sale_date) VALUES (%s, %s,NOW())", (product_id, quantity_sold,))
    
    connection.commit()
    connection.close()
    print("Sale recorded successfully.")
    return True

def view_sales():
    """Fetch sales records with product name and category."""
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()

    query = """
        SELECT s.sale_id, p.name, p.category, s.quantity_sold, s.sale_date 
        FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.sale_date DESC
    """
    cursor.execute(query)
    sales = cursor.fetchall()
    for sale in sales:
        print(sale)
    connection.close()
    return sales


def low_stock_alert(threshold=5):
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT id, name, quantity FROM products WHERE quantity < %s", (threshold,))
    low_stock_items = cursor.fetchall()
    connection.close()
    '''
    if low_stock_items:
        print("Low Stock Alert:")
        for item in low_stock_items:
            print(f"Product ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
    else:
        print("All products have sufficient stock.")
    '''
    return low_stock_items

def sales_over_time():
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    cursor.execute("SELECT sale_date, quantity_sold FROM sales")
    sales_data = cursor.fetchall()
    connection.close()
    
    dates, quantities = zip(*sales_data) if sales_data else ([], [])
    plt.figure(figsize=(8, 5))
    plt.plot(dates, quantities, marker='o', linestyle='-')
    plt.title("Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Quantity Sold")
    plt.xticks(rotation=45)
    plt.show()

def best_selling_categories():
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    cursor.execute("SELECT category, SUM(quantity_sold) FROM sales JOIN products ON sales.product_id = products.id GROUP BY category")
    category_data = cursor.fetchall()
    connection.close()
    
    categories, category_counts = zip(*category_data) if category_data else ([], [])
    plt.figure(figsize=(8, 5))
    plt.pie(category_counts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Best-Selling Categories")
    plt.show()


if __name__ == "__main__":
    choice = input("Do you want to record a sale, view sales, or check low stock? (r/v/l): ")
    if choice == 'r':
        product_id = int(input("Enter product ID: "))
        quantity_sold = int(input("Enter quantity sold: "))
        record_sale(product_id, quantity_sold)
    elif choice == 'v':
        view_sales()
    elif choice == 'l':
        low_stock_alert()
