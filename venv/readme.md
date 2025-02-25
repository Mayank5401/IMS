# Inventory Management System

## Overview
The Inventory Management System is a Python-based desktop application designed to streamline product tracking, sales recording, and user management. Built with **Tkinter** for the GUI and **MySQL** for data storage, this system provides an intuitive interface for both **administrators** and **staff members** to manage inventory efficiently.

## Key Features

### 🔹 **User Authentication & Role-Based Access**
- Secure login system.
- **Admins** can manage users, while **staff** have limited access.

### 📦 **Product Management**
- **Add, Edit, View, and Delete Products**
- Tracks product details including category, stock levels, and pricing.

### 📊 **Sales Management**
- **Record Sales Transactions**
- **View Past Sales Records**
- **Low Stock Alerts** notify users when inventory is running low.

### 📈 **Graphical Sales Dashboard**
- **Line Chart**: Tracks sales over time.
- **Pie Chart**: Displays best-selling categories.

### 🎨 **Enhanced User Interface**
- **Dynamic Theming**: Toggle between light and dark mode.
- **Scrollable Main Menu**: Ensures accessibility for all options.
- **Centralized Layout**: UI elements remain centered when resizing or scrolling.

### ⚙️ **Additional Functionalities**
- **Update User Profile**: Users can change their username and phone number.
- **Change PIN**: Allows users to reset their security PIN.
- **Delete Account**: Admins can remove users from the system.
- **Export Sales Report**: Generates PDF reports for business insights.

## Technologies Used
- **Python** (Tkinter for GUI)
- **MySQL** (Database for storing product, sales, and user information)
- **Matplotlib** (For graphical reports)
- **PIL (Pillow)** (For handling images in the UI)
- **FPDF** (For generating PDF reports)

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mayank5401/IMS.git
   cd inventory-management
   ```
2. **Install dependencies:**
   ```bash
   pip install mysql-connector-python tk pillow matplotlib fpdf
   ```
3. **Set up the MySQL database:**
   - Import the `inventory_db.sql` file into MySQL.
   - Update the `host`, `user`, and `password` in the Python scripts.

4. **Run the application:**
   ```bash
   python main.py
   ```

## Future Enhancements
- **Bar Graph for Monthly Sales Comparison**
- **Multi-Language Support**
- **Advanced User Analytics**
- **Cloud Database Integration**

## Contributors
- **[Mayank Pathak]** – Developer
- **Open for Contributions!** Feel free to submit pull requests.

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

---
🚀 **A powerful yet simple inventory management solution to streamline business operations!**

