import mysql.connector

def create_database():
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_db")
    connection.close()

def create_tables():
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL
                    )''')
                    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        category VARCHAR(50),
                        price DECIMAL(10,2) NOT NULL,
                        quantity INT NOT NULL CHECK (quantity >= 0)
                    )''')
                    
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        sale_id INT AUTO_INCREMENT PRIMARY KEY,
                        product_id INT,
                        quantity_sold INT,
                        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products(id)
                    )''')
                    
    connection.commit()
    connection.close()

# implement role based user access
query= " ALTER TABLE users ADD COLUMN role ENUM('admin', 'staff') NOT NULL DEFAULT 'staff'";


if __name__ == "__main__":
    create_database()
    create_tables()
    print("Database and tables created successfully.")
