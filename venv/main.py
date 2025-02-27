import tkinter as tk
from tkinter import Image, PhotoImage, messagebox, ttk
from auth import login_user, register_user, add_user, delete_user, edit_user, view_users
from products import add_product, view_products, delete_product, edit_product
from sales import record_sale, view_sales, low_stock_alert
from PIL import Image, ImageTk

# Define a universal background color
BACKGROUND_COLOR = "#f0f0f0"

def clear_screen():
    for widget in main_window.winfo_children():
        widget.destroy()
    main_window.configure(bg=BACKGROUND_COLOR)

def center_widget(widget):
    widget.pack(pady=5, padx=20)
    widget.pack_configure(anchor="center")

def login():

    global current_user_role
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password")
        return
    if username == "admin" and password == "admin":  # Default credentials for testing
        current_user_role = "admin"
        main_menu()
        return
    
    role = login_user(username, password)

    if role :
        messagebox.showinfo("Success", f"Login successful as {role}")
        current_user_role = role  # Store user role
        main_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def register():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password")
        return
    if register_user(username, password):
        messagebox.showinfo("Success", "User registered successfully. Please login.")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Registration failed. Try again.")

def view_products_ui():
    clear_screen()
    
    tk.Label(main_window, text="Product List", font=("Arial", 16, "bold")).pack(pady=10)
    
    products = view_products()  # Fetch products from the database
    
    if not products:
        messagebox.showinfo("No Products", "No products available in inventory.")
        main_menu()
        return

    # Create a frame for the table
    table_frame = tk.Frame(main_window,  bg=BACKGROUND_COLOR)
    table_frame.pack(pady=10)

    # Define table columns
    columns = ("ID", "Name", "Category", "Price($)", "Quantity")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Define column headings with styling
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=120, anchor="center")

    # Insert product data into the table
    for product in products:
        tree.insert("", "end", values=product)

    # Add table styles
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#f2f2f2", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#007acc", foreground="black")
    style.map("Treeview", background=[("selected", "#4caf50")])  # Highlight selected row in green

    tree.pack()

    # Add Back button
    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)

def add_product_ui():
    clear_screen()
    
    tk.Label(main_window, text="Add Product", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)

    tk.Label(main_window, text="Product Name:", font=("Arial", 12),bg=BACKGROUND_COLOR).pack()
    name_entry = tk.Entry(main_window)
    center_widget(name_entry)

    tk.Label(main_window, text="Category:", font=("Arial", 12),bg=BACKGROUND_COLOR).pack()
    category_entry = tk.Entry(main_window)
    center_widget(category_entry)

    tk.Label(main_window, text="Quantity:", font=("Arial", 12), bg=BACKGROUND_COLOR).pack()
    quantity_entry = tk.Entry(main_window)
    center_widget(quantity_entry)

    tk.Label(main_window, text="Price:", font=("Arial", 12), bg=BACKGROUND_COLOR).pack()
    price_entry = tk.Entry(main_window)
    center_widget(price_entry)

    def submit():
        name = name_entry.get()
        category = category_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if not name or not category or not quantity or not price:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        
        if not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showwarning("Input Error", "Quantity and Price must be numeric")
            return

        add_product(name, category, int(quantity), float(price))
        messagebox.showinfo("Success", "Product added successfully")
        main_menu()

    tk.Button(main_window, text="Add Product", command=submit, font=("Arial", 12), bg="#28a745", fg="white").pack(pady=5)
    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)


def delete_product_ui():
    clear_screen()

    tk.Label(main_window, text="Delete Product", font=("Arial", 16, "bold"), bg="#e1e1e1").pack(pady=10)

    tk.Label(main_window, text="Product ID:", font=("Arial", 12)).pack()
    id_entry = tk.Entry(main_window)
    center_widget(id_entry)

    def submit():
        product_id = id_entry.get()
        
        if not product_id.isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid numeric Product ID")
            return

        delete_product(int(product_id))
        messagebox.showinfo("Success", "Product deleted successfully")
        main_menu()

    tk.Button(main_window, text="Delete Product", command=submit, font=("Arial", 12), bg="#dc3545", fg="white").pack(pady=5)
    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)


def edit_product_ui():
    clear_screen()

    tk.Label(main_window, text="Edit Product", font=("Arial", 16, "bold"), bg="#e1e1e1").pack(pady=10)

    tk.Label(main_window, text="Product ID:", font=("Arial", 12)).pack()
    id_entry = tk.Entry(main_window)
    center_widget(id_entry)

    tk.Label(main_window, text="New Name:", font=("Arial", 12)).pack()
    name_entry = tk.Entry(main_window)
    center_widget(name_entry)

    tk.Label(main_window, text="New Category:", font=("Arial", 12)).pack()
    category_entry = tk.Entry(main_window)
    center_widget(category_entry)

    tk.Label(main_window, text="New Quantity:", font=("Arial", 12)).pack()
    quantity_entry = tk.Entry(main_window)
    center_widget(quantity_entry)

    tk.Label(main_window, text="New Price:", font=("Arial", 12)).pack()
    price_entry = tk.Entry(main_window)
    center_widget(price_entry)

    def submit():
        product_id = id_entry.get()
        name = name_entry.get()
        category = category_entry.get()
        quantity = quantity_entry.get()
        price = price_entry.get()

        if not product_id.isdigit():
            messagebox.showwarning("Input Error", "Product ID must be numeric")
            return
        
        if quantity and not quantity.isdigit():
            messagebox.showwarning("Input Error", "Quantity must be numeric")
            return

        if price and not price.replace('.', '', 1).isdigit():
            messagebox.showwarning("Input Error", "Price must be numeric")
            return

        edit_product(int(product_id), name if name else None, category if category else None, int(quantity) if quantity else None, float(price) if price else None)
        messagebox.showinfo("Success", "Product updated successfully")
        main_menu()

    tk.Button(main_window, text="Edit Product", command=submit, font=("Arial", 12), bg="#ffc107", fg="black").pack(pady=5)
    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)

def record_sale_ui():
    clear_screen()
    
    tk.Label(main_window, text="Record Sale", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)

    tk.Label(main_window, text="Product ID:", font=("Arial", 12), bg=BACKGROUND_COLOR).pack()
    product_id_entry = tk.Entry(main_window)
    product_id_entry.pack(pady=5)

    tk.Label(main_window, text="Quantity:", font=("Arial", 12), bg=BACKGROUND_COLOR).pack()
    quantity_entry = tk.Entry(main_window)
    quantity_entry.pack(pady=5)

    def submit_sale():
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()
        
        if not product_id or not quantity:
            messagebox.showwarning("Input Error", "Please enter Product ID and Quantity.")
            return
        
        if record_sale(product_id, int(quantity)):  
            messagebox.showinfo("Success", "Sale recorded successfully.")
            main_menu()
        else:
            messagebox.showerror("Error", "Sale could not be recorded. Check stock levels.")

    tk.Button(main_window, text="Submit", command=submit_sale, font=("Arial", 12), bg="#28a745", fg="white").pack(pady=5)
    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=5)

def view_sales_ui():
    
    clear_screen()
    
    tk.Label(main_window, text="Sales Records", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)
    
    sales = view_sales()  # Fetch sales records from the database

    if not sales:
        messagebox.showinfo("No Sales", "No sales records available.")
        main_menu()
        return

    # Create a frame for the table
    table_frame = tk.Frame(main_window)
    table_frame.pack(pady=10)

    # Define table columns
    columns = ("Serial No", "Name","Category", "Quantity", "TimeStamp")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    # Define column headings with styling
    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=120, anchor="center")

    for i, sale in enumerate(sales, start=1):
        id,product_name, category, quantity_sold,sale_date = sale
        tree.insert("", "end", values=(i, product_name, category, quantity_sold, sale_date))
    '''
    # Insert sales data into the table
    for sale in sales:
        tree.insert("", "end", values=sale)
    '''
    # Add table styles
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#007acc", foreground="black")
    style.map("Treeview", background=[("selected", "#4caf50")])  # Highlight selected row in green

    tree.pack()

    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)

def low_stock_alert_ui():
    """UI for viewing low-stock products."""
    clear_screen()

    tk.Label(main_window, text="Low Stock Products", font=("Arial", 16, "bold"), bg=BACKGROUND_COLOR).pack(pady=10)

    low_stock_items = low_stock_alert()  # Get low stock products

    if not low_stock_items:
        messagebox.showinfo("Stock Status", "No low-stock products.")
        main_menu()
        return

    table_frame = tk.Frame(main_window)
    table_frame.pack(pady=10)

    columns = ("Product ID", "Name", "Qty Sold")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    for col in columns:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=120, anchor="center")

    for item in low_stock_items:
        tree.insert("", "end", values=item)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#ff9800", foreground="black")
    style.map("Treeview", background=[("selected", "#ffcc80")])  # Highlight selected row in orange

    tree.pack()

    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)

def main_menu():
    clear_screen()
    tk.Label(main_window, text="Inventory Management", font=("Calibri", 20, "bold"), fg= "black").pack(pady=10)
    
    if current_user_role == "admin":
    
        buttons = [
            ("Add Product", add_product_ui),
            ("View Products", view_products_ui),
            ("Edit Products", edit_product_ui),
            ("Delete Product", delete_product_ui),
            ("Record Sale", record_sale_ui),
            ("View Sales", view_sales_ui),
            ("Low Stock Alert", low_stock_alert_ui),
            ("Manage Users", manage_users_ui),
            ("Back", login_ui),
            ("Exit", main_window.quit)
        ]
    else: # for staff
        buttons = [
            ("Record Sale", record_sale_ui),
            ("View Products", view_products_ui),
            ("Edit Products", edit_product_ui),
            ("View Sales", view_sales_ui),
            ("Low Stock Alert", low_stock_alert_ui),
            ("Back", login_ui),
            ("Exit", main_window.quit)
        ]
    
    for text, command in buttons:
        tk.Button(main_window, text=text, command=command, font=("Arial", 12), width=20, height=2, bg="#007acc", fg="white").pack(pady=5)

def manage_users_ui():
    clear_screen()
    tk.Label(main_window, text="Manage Users", font=("Arial", 16, "bold"), bg="#e1e1e1").pack(pady=10)

    users = view_users()

    tree = ttk.Treeview(main_window, columns=("ID", "Username", "Role"), show="headings")
    tree.heading("ID", text="User ID")
    tree.heading("Username", text="Username")
    tree.heading("Role", text="Role")

    for user in users:
        tree.insert("", "end", values=user)

    tree.pack(pady=10)

    # Fields for adding/editing users
    tk.Label(main_window, text="Username:").pack()
    username_entry = tk.Entry(main_window)
    username_entry.pack()

    tk.Label(main_window, text="Password:").pack()
    password_entry = tk.Entry(main_window, show="*")
    password_entry.pack()

    tk.Label(main_window, text="Role:").pack()
    role_var = tk.StringVar(value="staff")
    role_menu = tk.OptionMenu(main_window, role_var, "admin", "staff")
    role_menu.pack()

    def add_user_action():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and Password cannot be empty")
            return

        if add_user(username, password, role):
            messagebox.showinfo("Success", "User added successfully")
            manage_users_ui()  # Refresh screen
        else:
            messagebox.showerror("Error", "Username already exists")

    tk.Button(main_window, text="Add User", command=add_user_action, bg="green", fg="white").pack(pady=5)

    # Back button
    tk.Button(main_window, text="Back", command=main_menu, bg="gray", fg="white").pack(pady=5)

def login_ui():
    clear_screen()
    '''
    # Load and display logo
    try:
        logo_image = Image.open("venv\inv_logo.png") 
        logo_label = tk.Label(main_window, image=logo_image, bg="#e1e1e1")
        logo_label.image = ImageTk.PhotoImage(logo_image) 
        logo_label.pack()
    except Exception as e:
         messagebox.showerror("Image Error", f"Error loading logo: {e}")
    '''

    tk.Label(main_window, text="Username:", font=("Arial", 12), bg="#f8f9fa").pack()
    global username_entry
    username_entry = tk.Entry(main_window)
    username_entry.insert(0, "admin")  # Pre-fill with default username
    center_widget(username_entry)
    
    tk.Label(main_window, text="Password:", font=("Arial", 12), bg="#f8f9fa").pack()
    global password_entry
    password_entry = tk.Entry(main_window, show="*")
    password_entry.insert(0, "admin")  # Pre-fill with default password
    center_widget(password_entry)
    
    tk.Button(main_window, text="Login", command=login, font=("Arial", 12), bg="#007bff", fg="white").pack(pady=5)
    tk.Button(main_window, text="Register", command=register, font=("Arial", 12), bg="#28a745", fg="white").pack()

def start_app():
    global main_window
    main_window = tk.Tk()
    main_window.title("Inventory Management System")
    main_window.geometry("600x500")
    main_window.configure(bg="#f8f9fa")
    login_ui()
    main_window.mainloop()

start_app()
