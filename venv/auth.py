import mysql.connector
import bcrypt

def register_user(username, password):

    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        print("User registered successfully.")
        return True
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    
    finally:
        connection.close()

def login_user(username, password):
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT password_hash, role FROM users WHERE username = %s " , (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        print("Login successful.")
        return user[1]
    else:
        print("Invalid username or password.")
        return None
    
def add_user(username, password, role):
    
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        connection.commit()
        return True
    except mysql.connector.IntegrityError:
        return False  # Username already exists
    finally:
        connection.close()

def view_users():
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    connection.close()
    return users

def edit_user(user_id, new_role):
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    connection.commit()
    connection.close()

def delete_user(user_id):
    connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()
    connection.close()




if __name__ == "__main__":
    choice = input("Do you want to register or login? (r/l): ")
    if choice == 'r':
        username = input("Enter username: ")
        password = input("Enter password: ")
        register_user(username, password)
    elif choice == 'l':
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_user(username, password)
