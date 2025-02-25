import tkinter as tk
from tkinter import Image, PhotoImage, messagebox, ttk
from auth import login_user, register_user, add_user, delete_user, edit_user, view_users
from products import add_product, view_products, delete_product, edit_product
from sales import record_sale, view_sales, low_stock_alert ,best_selling_categories,sales_over_time
from PIL import Image, ImageTk
import csv ,matplotlib.pyplot as plt
import mysql
from fpdf import FPDF

# Define a universal background color
BACKGROUND_COLOR = "#f0f0f0"

dark_mode = False  # Track theme state
bg_color = "#f8f9fa"
fg_color = "black"

def toggle_theme():
    global dark_mode, bg_color, fg_color
    dark_mode = not dark_mode
    bg_color = "#2c2c2c" if dark_mode else "#f8f9fa"
    fg_color = "white" if dark_mode else "black"
    
    apply_theme()

def apply_theme():
  
    main_window.configure(bg=bg_color)
    for widget in main_window.winfo_children():
        try:
            widget.configure(bg=bg_color, fg=fg_color)
        except:
            pass

 
def clear_screen():
    main_window.unbind_all("<MouseWheel>")  

    for widget in main_window.winfo_children():
        widget.destroy()
    apply_theme()

def center_widget(widget):
    widget.pack(pady=5, padx=20)
    widget.pack_configure(anchor="center")

def download_sales_summary():
    sales = view_sales()
    if not sales:
        messagebox.showwarning("No Data", "No sales data available to export.")
        return
    
    with open("sales_summary.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sale ID", "Product Name", "Category", "Quantity Sold", "Sale Date"])
        writer.writerows(sales)
    
    messagebox.showinfo("Success", "Sales summary downloaded as CSV.")

def generate_sales_chart():
    sales = view_sales()
    if not sales:
        messagebox.showwarning("No Data", "No sales data available for visualization.")
        return
    
    product_sales = {}
    for sale in sales:
        product_name = sale[1]
        quantity_sold = sale[3]
        product_sales[product_name] = product_sales.get(product_name, 0) + quantity_sold
    
    plt.figure(figsize=(8, 5))
    plt.bar(product_sales.keys(), product_sales.values(), color="#007acc")
    plt.xlabel("Product Name")
    plt.ylabel("Quantity Sold")
    plt.title("Sales Trends")
    plt.xticks(rotation=45)
    plt.show()


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
    
    tk.Label(main_window, text="Product List", font=("Arial", 16, "bold"),bg=bg_color, fg=fg_color).pack(pady=10)
    
    products = view_products()  # Fetch products from the database
    
    if not products:
        messagebox.showinfo("No Products", "No products available in inventory.")
        main_menu()
        return

    # Create a frame for the table
    table_frame = tk.Frame(main_window,  bg=BACKGROUND_COLOR)
    table_frame.pack(pady=10)

    # Define table columns
    columns = ("ID", "Name", "Category", "Price(Rs)", "Quantity")

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
    
    tk.Label(main_window, text="Add Product", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=10)

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

    tk.Label(main_window, text="Delete Product", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=10)

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

def generate_invoice(sale):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Invoice Number: {sale[0]}", ln=True)
    pdf.cell(200, 10, txt=f"Product: {sale[1]}", ln=True)
    pdf.cell(200, 10, txt=f"Category: {sale[2]}", ln=True)
    pdf.cell(200, 10, txt=f"Quantity Sold: {sale[3]}", ln=True)
    pdf.cell(200, 10, txt=f"Sale Date: {sale[4]}", ln=True)
    pdf.output(f"invoice_{sale[0]}.pdf")
    messagebox.showinfo("Invoice Generated", f"Invoice saved as invoice_{sale[0]}.pdf")

def view_sales_ui():
    
    clear_screen()
    tk.Label(main_window, text="View Sales", font=("Arial", 16, "bold"), bg=bg_color, fg= fg_color).pack(pady=10)
    
    filter_frame = tk.Frame(main_window, bg=main_window.cget("bg"))
    filter_frame.pack(pady=5)
    
    tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):", bg=bg_color, fg= fg_color).grid(row=0, column=0)
    start_date_entry = tk.Entry(filter_frame)
    start_date_entry.grid(row=0, column=1, padx=5)
    
    tk.Label(filter_frame, text="End Date (YYYY-MM-DD):", bg=bg_color, fg= fg_color).grid(row=0, column=2)
    end_date_entry = tk.Entry(filter_frame)
    end_date_entry.grid(row=0, column=3, padx=5)
    
    tk.Label(filter_frame, text="Category:", bg=bg_color, fg= fg_color).grid(row=0, column=4)
    category_entry = tk.Entry(filter_frame)
    category_entry.grid(row=0, column=5, padx=5)
    
    def apply_filters():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        category = category_entry.get()
        
        conditions = []
        params = []
        
        if start_date:
            conditions.append("sale_date >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("sale_date <= %s")
            params.append(end_date)
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        where_clause = " AND ".join(conditions) if conditions else "1"
        query = f"SELECT sales.sale_id, products.name, products.category, sales.quantity_sold, sales.sale_date FROM sales JOIN products ON sales.product_id = products.id WHERE {where_clause}"
        
        connection = mysql.connector.connect(host='localhost', user='Mayank', password='Rcf@634e', database='inventory_db')
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        filtered_sales = cursor.fetchall()
        connection.close()
        
        update_sales_table(filtered_sales)
    
    tk.Button(filter_frame, text="Apply Filters", command=apply_filters, bg="#007acc", fg="white").grid(row=0, column=6, padx=5)
    
    columns = ("#", "Product Name", "Category", "Quantity Sold", "Sale Date")
    sales_table = ttk.Treeview(main_window, columns=columns, show="headings")
    sales_table.pack(pady=10, padx=10, expand=True)
    
    for col in columns:
        sales_table.heading(col, text=col)
        sales_table.column(col, anchor="center", width=150)
    
    total_label = tk.Label(main_window, text="", font=("Arial", 12, "bold"), bg=main_window.cget("bg"), fg="black")
    total_label.pack()

    def update_sales_table(sales):
        for row in sales_table.get_children():
            sales_table.delete(row)
        total_quantity = 0
        for i, sale in enumerate(sales, start=1):
            sales_table.insert("", "end", values=(i, sale[1], sale[2], sale[3], sale[4]))
            total_quantity += sale[3]
        total_label.config(text=f"Total Quantity Sold: {total_quantity}")

    def on_invoice_click(event):
        selected_item = sales_table.selection()
        if selected_item:
#            sale = sales_table.item(selected_item, "tags")[0]
            sale_values = sales_table.item(selected_item, "values")
            if sale_values:
                sale = (sale_values[0], sale_values[1], sale_values[2], sale_values[3], sale_values[4])
                generate_invoice(sale)

    
    sales_table.bind("<Double-1>", on_invoice_click)
    
    sales = view_sales()
    update_sales_table(sales)
    
    
    # Add table styles
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#007acc", foreground="black")
    style.map("Treeview", background=[("selected", "#4caf50")])  # Highlight selected row in green

    sales_table.pack()
    
    tk.Button(main_window, text="Download Sales Summary",command=download_sales_summary,font=("Arial", 12), width=25, height=2, bg=bg_color, fg=fg_color).pack(pady=10)
    tk.Button(main_window, text="Generate Sales Chart",command=generate_sales_chart,font=("Arial", 12), width=25, height=2, bg=bg_color, fg=fg_color).pack(padx=10)
    tk.Button(main_window, text="Back", command=main_menu, font=("Arial", 12), bg="#007acc", fg="white").pack(pady=10)

def low_stock_alert_ui():
    """UI for viewing low-stock products."""
    clear_screen()

    tk.Label(main_window, text="Low Stock Products", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=10)

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
    apply_theme()

    # Create a container for canvas + scrollbar
    container = tk.Frame(main_window)
    container.pack(fill=tk.BOTH, expand=True)

    # Create a canvas
    canvas = tk.Canvas(container, bg=bg_color)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add vertical scrollbar
    scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    # Place frame inside the canvas but anchored to the TOP LEFT
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def update_scroll_region(event):
        """Ensures the canvas updates its scroll region dynamically."""
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(window_id, width=canvas.winfo_width())  # Adjust width

    # Bind the resize event to adjust scroll region
    scrollable_frame.bind("<Configure>", update_scroll_region)

    # Center the frame's content
    inner_frame = tk.Frame(scrollable_frame, bg=bg_color)
    inner_frame.pack(anchor="center")  # Keeps content centered

    # Title Label - CENTERED
    tk.Label(inner_frame, text="Inventory Management", font=("Calibri", 20, "bold"), fg=fg_color, bg=bg_color).pack(pady=10)

    # Define buttons based on user role
    buttons = [
        ("Add Product", add_product_ui),
        ("View Products", view_products_ui),
        ("Edit Products", edit_product_ui),
        ("Delete Product", delete_product_ui),
        ("Record Sale", record_sale_ui),
        ("View Sales", view_sales_ui),
        ("Low Stock Alert", low_stock_alert_ui),
        ("Sales Dashboard", sales_dashboard_ui),
        ("Manage Users", manage_users_ui),
        ("Toggle Theme", toggle_theme),
        ("Back", login_ui),
        ("Exit", main_window.quit)
    ] if current_user_role == "admin" else [
        ("Record Sale", record_sale_ui),
        ("View Products", view_products_ui),
        ("Edit Products", edit_product_ui),
        ("View Sales", view_sales_ui),
        ("Low Stock Alert", low_stock_alert_ui),
        ("Sales Dashboard", sales_dashboard_ui),
        ("Toggle Theme", toggle_theme),
        ("Back", login_ui),
        ("Exit", main_window.quit)
    ]

    # Add buttons in a loop, CENTERED inside `inner_frame`
    for text, command in buttons:
        tk.Button(inner_frame, text=text, command=command, font=("Arial", 12), width=20, height=2, bg="#007acc", fg=fg_color).pack(pady=5, anchor="center")

    # Enable mouse scrolling
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units") if scrollable_frame.winfo_exists() else None)

def sales_dashboard_ui():
    clear_screen()
    tk.Label(main_window, text="Sales Dashboard", font=("Arial", 16, "bold"), bg=bg_color, fg =fg_color, anchor="center").pack(pady=10)
    
    tk.Button(main_window, text="Line Chart - Sales Over Time", command=sales_over_time, bg=bg_color, fg =fg_color, anchor="center").pack(pady=5)
    tk.Button(main_window, text="Pie Chart - Best-Selling Categories", command=best_selling_categories,bg=bg_color, fg =fg_color, anchor="center").pack(pady=5)
#   tk.Button(main_window, text="Bar Chart - Monthly Sales Comparison", command=sales_dashboard, bg="#007acc", fg="white").pack(pady=5)
    tk.Button(main_window, text="Back", command=view_sales_ui, bg=bg_color, fg =fg_color, anchor="center").pack(pady=5)

def manage_users_ui():
    clear_screen()
    users = view_users()
    tk.Label(main_window, text="Manage Users", font=("Arial", 16, "bold"), bg=bg_color, fg=fg_color).pack(pady=10)
    
    tree = ttk.Treeview(main_window, columns=("ID", "Username", "Role"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Role", text="Role")
    
    tree.column("ID", width=50, anchor="center")
    tree.column("Username", width=150, anchor="center")
    tree.column("Role", width=100, anchor="center")
    
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), background="white", foreground="black", rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#007acc", foreground="black")
    
    tree.pack(pady=10)
    for user in users:
        tree.insert("", "end", values=user)

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
    tk.Label(main_window, text="Login", font=("Arial", 16, "bold"), bg=main_window.cget("bg"), fg="black").pack(pady=10)
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
