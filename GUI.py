import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime

class EcommercePlatform:
    def __init__(self):
        # In-memory data structures
        self.vendors = []
        self.products = []
        self.customers = []
        self.orders = []
        self.order_items = []
        
        self.current_user = None
        self.current_order = None
        
        # Add sample data
        self.add_sample_data()
    
    def add_sample_data(self):
        # Add sample vendors
        vendor1_id = self.add_vendor("TechGadgets", "Global")
        vendor2_id = self.add_vendor("FashionHub", "North America, Europe")
        vendor3_id = self.add_vendor("HomeEssentials", "Asia, Australia")
        
        # Add sample products
        self.add_product(vendor1_id, "Smartphone X", 599.99, "Electronics", "Phone", "5G")
        self.add_product(vendor1_id, "Wireless Earbuds", 129.99, "Audio", "Wireless", "Bluetooth")
        self.add_product(vendor2_id, "Designer Jeans", 89.99, "Clothing", "Denim", "Fashion")
        self.add_product(vendor2_id, "Leather Jacket", 199.99, "Outerwear", "Leather", "Winter")
        self.add_product(vendor3_id, "Coffee Maker", 49.99, "Kitchen", "Coffee", "Appliance")
        
        # Add sample customer
        self.add_customer("John Doe", "555-123-4567", "123 Main St, Anytown, USA")
    
    # Vendor Administration Functions
    def list_all_vendors(self):
        return self.vendors
    
    def add_vendor(self, business_name, geographical_presence):
        vendor_id = len(self.vendors) + 1
        self.vendors.append({
            'vendor_id': vendor_id,
            'business_name': business_name,
            'feedback_score': 0.0,
            'geographical_presence': geographical_presence
        })
        return vendor_id
    
    # Product Catalog Management Functions
    def list_vendor_products(self, vendor_id):
        return [p for p in self.products if p['vendor_id'] == vendor_id]
    
    def add_product(self, vendor_id, name, price, tag1=None, tag2=None, tag3=None):
        product_id = len(self.products) + 1
        self.products.append({
            'product_id': product_id,
            'vendor_id': vendor_id,
            'name': name,
            'price': price,
            'tag1': tag1,
            'tag2': tag2,
            'tag3': tag3
        })
        return product_id
    
    # Product Discovery Function
    def search_products(self, search_term):
        search_term = search_term.lower()
        results = []
        
        for product in self.products:
            # Get vendor name
            vendor_name = next((v['business_name'] for v in self.vendors if v['vendor_id'] == product['vendor_id']), "Unknown")
            
            # Check if search term matches name or tags
            if (search_term in product['name'].lower() or
                (product['tag1'] and search_term in product['tag1'].lower()) or
                (product['tag2'] and search_term in product['tag2'].lower()) or
                (product['tag3'] and search_term in product['tag3'].lower())):
                
                result = product.copy()
                result['vendor_name'] = vendor_name
                results.append(result)
                
        return results
    
    # Customer Management Functions
    def add_customer(self, name, contact_number, shipping_address):
        customer_id = len(self.customers) + 1
        self.customers.append({
            'customer_id': customer_id,
            'name': name,
            'contact_number': contact_number,
            'shipping_address': shipping_address
        })
        return customer_id
    
    def get_customer(self, customer_id):
        return next((c for c in self.customers if c['customer_id'] == customer_id), None)
    
    # Order Management Functions
    def create_order(self, customer_id):
        order_id = len(self.orders) + 1
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.orders.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'order_date': current_date,
            'status': 'pending'
        })
        return order_id
    
    def add_to_order(self, order_id, product_id, vendor_id, quantity=1):
        order_item_id = len(self.order_items) + 1
        
        self.order_items.append({
            'order_item_id': order_item_id,
            'order_id': order_id,
            'product_id': product_id,
            'vendor_id': vendor_id,
            'quantity': quantity
        })
        return order_item_id
    
    def get_order_items(self, order_id):
        items = []
        for item in self.order_items:
            if item['order_id'] == order_id:
                # Get product and vendor details
                product = next((p for p in self.products if p['product_id'] == item['product_id']), None)
                vendor = next((v for v in self.vendors if v['vendor_id'] == item['vendor_id']), None)
                
                if product and vendor:
                    item_details = item.copy()
                    item_details['product_name'] = product['name']
                    item_details['price'] = product['price']
                    item_details['vendor_name'] = vendor['business_name']
                    items.append(item_details)
        
        return items
    
    def remove_from_order(self, order_item_id):
        self.order_items = [item for item in self.order_items if item['order_item_id'] != order_item_id]
    
    def cancel_order(self, order_id):
        for order in self.orders:
            if order['order_id'] == order_id:
                order['status'] = 'cancelled'
                break
    
    def get_customer_orders(self, customer_id):
        customer_orders = [order for order in self.orders if order['customer_id'] == customer_id]
        # Sort by date (newest first)
        customer_orders.sort(key=lambda x: x['order_date'], reverse=True)
        return customer_orders


class EcommerceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Vendor Ecommerce Platform")
        self.root.geometry("800x600")
        
        self.platform = EcommercePlatform()
        
        # Set up the initial login/register screen
        self.setup_login_screen()
    
    def setup_login_screen(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Multi-Vendor Ecommerce Platform", font=("Arial", 16)).pack(pady=10)
        
        ttk.Button(frame, text="Login as Customer", command=self.login_as_customer).pack(pady=5, fill='x')
        ttk.Button(frame, text="Register as Customer", command=self.register_customer).pack(pady=5, fill='x')
        ttk.Button(frame, text="Vendor Management", command=self.vendor_management).pack(pady=5, fill='x')
        ttk.Button(frame, text="Exit", command=self.root.destroy).pack(pady=5, fill='x')
    
    def login_as_customer(self):
        customer_id = simpledialog.askinteger("Login", "Enter your Customer ID:")
        if customer_id:
            customer = self.platform.get_customer(customer_id)
            if customer:
                self.platform.current_user = customer
                self.setup_customer_dashboard()
            else:
                messagebox.showerror("Error", "Customer not found")
    
    def register_customer(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Register as Customer", font=("Arial", 16)).pack(pady=10)
        
        ttk.Label(frame, text="Name:").pack(anchor='w')
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(frame, text="Contact Number:").pack(anchor='w')
        contact_var = tk.StringVar()
        ttk.Entry(frame, textvariable=contact_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(frame, text="Shipping Address:").pack(anchor='w')
        address_var = tk.StringVar()
        ttk.Entry(frame, textvariable=address_var, width=40).pack(pady=5, fill='x')
        
        def submit_registration():
            name = name_var.get()
            contact = contact_var.get()
            address = address_var.get()
            
            if name and contact and address:
                customer_id = self.platform.add_customer(name, contact, address)
                messagebox.showinfo("Success", "Registration successful! Your Customer ID is: {}".format(customer_id))
                self.platform.current_user = self.platform.get_customer(customer_id)
                self.setup_customer_dashboard()
            else:
                messagebox.showerror("Error", "All fields are required")
        
        ttk.Button(frame, text="Register", command=submit_registration).pack(pady=10)
        ttk.Button(frame, text="Back", command=self.setup_login_screen).pack()
    
    def setup_customer_dashboard(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)
        
        customer = self.platform.current_user
        ttk.Label(frame, text="Welcome, {}!".format(customer['name']), font=("Arial", 16)).pack(pady=10)
        
        # Create notebook (tabbed interface)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Product Search
        search_tab = ttk.Frame(notebook, padding=10)
        notebook.add(search_tab, text="Search Products")
        
        search_frame = ttk.Frame(search_tab)
        search_frame.pack(fill='x', pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=search_var, width=40).pack(side='left', padx=5)
        
        # Create treeview for search results
        columns = ('ID', 'Name', 'Price', 'Vendor', 'Tags')
        search_tree = ttk.Treeview(search_tab, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            search_tree.heading(col, text=col)
            search_tree.column(col, width=100)
        
        search_tree.pack(fill='both', expand=True)
        
        def search_products():
            search_term = search_var.get()
            if search_term:
                # Clear previous results
                for item in search_tree.get_children():
                    search_tree.delete(item)
                
                results = self.platform.search_products(search_term)
                for product in results:
                    tags = [tag for tag in [product['tag1'], product['tag2'], product['tag3']] if tag]
                    search_tree.insert('', 'end', values=(
                        product['product_id'],
                        product['name'],
                        "${:.2f}".format(product['price']),
                        product['vendor_name'],
                        ", ".join(tags)
                    ))
        
        def add_to_cart():
            selected_item = search_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a product")
                return
            
            values = search_tree.item(selected_item, 'values')
            product_id = int(values[0])
            
            # If no current order, create one
            if not self.platform.current_order:
                order_id = self.platform.create_order(customer['customer_id'])
                self.platform.current_order = order_id
            
            # Get vendor ID for the product
            product = next((p for p in self.platform.products if p['product_id'] == product_id), None)
            if product:
                # Add to order
                self.platform.add_to_order(self.platform.current_order, product_id, product['vendor_id'])
                messagebox.showinfo("Success", "Product added to cart")
            else:
                messagebox.showerror("Error", "Product not found")
        
        button_frame = ttk.Frame(search_tab)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Search", command=search_products).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Add to Cart", command=add_to_cart).pack(side='left', padx=5)
        
        # Tab 2: Cart / Current Order
        cart_tab = ttk.Frame(notebook, padding=10)
        notebook.add(cart_tab, text="Shopping Cart")
        
        # Create treeview for cart items
        cart_columns = ('Item ID', 'Product', 'Price', 'Vendor', 'Quantity')
        cart_tree = ttk.Treeview(cart_tab, columns=cart_columns, show='headings')
        
        # Define headings
        for col in cart_columns:
            cart_tree.heading(col, text=col)
            cart_tree.column(col, width=100)
        
        cart_tree.pack(fill='both', expand=True)
        
        def refresh_cart():
            # Clear previous items
            for item in cart_tree.get_children():
                cart_tree.delete(item)
            
            if self.platform.current_order:
                items = self.platform.get_order_items(self.platform.current_order)
                for item in items:
                    cart_tree.insert('', 'end', values=(
                        item['order_item_id'],
                        item['product_name'],
                        "${:.2f}".format(item['price']),
                        item['vendor_name'],
                        item['quantity']
                    ))
        
        def remove_from_cart():
            selected_item = cart_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an item to remove")
                return
            
            item_id = int(cart_tree.item(selected_item, 'values')[0])
            self.platform.remove_from_order(item_id)
            refresh_cart()
            messagebox.showinfo("Success", "Item removed from cart")
        
        def cancel_order():
            if self.platform.current_order:
                self.platform.cancel_order(self.platform.current_order)
                self.platform.current_order = None
                refresh_cart()
                messagebox.showinfo("Success", "Order cancelled")
            else:
                messagebox.showinfo("Info", "No active order to cancel")
        
        def checkout():
            if self.platform.current_order:
                # Update order status to completed
                for order in self.platform.orders:
                    if order['order_id'] == self.platform.current_order:
                        order['status'] = 'completed'
                        break
                
                messagebox.showinfo("Success", "Order completed successfully!")
                self.platform.current_order = None
                refresh_cart()
            else:
                messagebox.showinfo("Info", "No items in cart to checkout")
        
        cart_button_frame = ttk.Frame(cart_tab)
        cart_button_frame.pack(fill='x', pady=10)
        
        ttk.Button(cart_button_frame, text="Refresh Cart", command=refresh_cart).pack(side='left', padx=5)
        ttk.Button(cart_button_frame, text="Remove Item", command=remove_from_cart).pack(side='left', padx=5)
        ttk.Button(cart_button_frame, text="Cancel Order", command=cancel_order).pack(side='left', padx=5)
        ttk.Button(cart_button_frame, text="Checkout", command=checkout).pack(side='left', padx=5)
        
        # Tab 3: Order History
        history_tab = ttk.Frame(notebook, padding=10)
        notebook.add(history_tab, text="Order History")
        
        # Create treeview for order history
        history_columns = ('Order ID', 'Date', 'Status')
        history_tree = ttk.Treeview(history_tab, columns=history_columns, show='headings')
        
        # Define headings
        for col in history_columns:
            history_tree.heading(col, text=col)
        
        history_tree.pack(fill='both', expand=True)
        
        def load_order_history():
            # Clear previous items
            for item in history_tree.get_children():
                history_tree.delete(item)
            
            orders = self.platform.get_customer_orders(customer['customer_id'])
            for order in orders:
                history_tree.insert('', 'end', values=(
                    order['order_id'],
                    order['order_date'],
                    order['status']
                ))
        
        def view_order_details():
            selected_item = history_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an order to view")
                return
            
            order_id = int(history_tree.item(selected_item, 'values')[0])
            items = self.platform.get_order_items(order_id)
            
            # Create a pop-up window with order details
            details_window = tk.Toplevel(self.root)
            details_window.title("Order Details")
            details_window.geometry("600x400")
            
            ttk.Label(details_window, text="Order #{} Details".format(order_id), font=("Arial", 14)).pack(pady=10)
            
            # Create treeview for order items
            columns = ('Product', 'Price', 'Vendor', 'Quantity')
            details_tree = ttk.Treeview(details_window, columns=columns, show='headings')
            
            # Define headings
            for col in columns:
                details_tree.heading(col, text=col)
            
            details_tree.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Insert order items
            for item in items:
                details_tree.insert('', 'end', values=(
                    item['product_name'],
                    "${:.2f}".format(item['price']),
                    item['vendor_name'],
                    item['quantity']
                ))
            
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
        
        history_button_frame = ttk.Frame(history_tab)
        history_button_frame.pack(fill='x', pady=10)
        
        ttk.Button(history_button_frame, text="Load Order History", command=load_order_history).pack(side='left', padx=5)
        ttk.Button(history_button_frame, text="View Details", command=view_order_details).pack(side='left', padx=5)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill='x', pady=10)
        
        ttk.Button(bottom_frame, text="Logout", command=self.setup_login_screen).pack(side='right')
    
    def vendor_management(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Vendor Management", font=("Arial", 16)).pack(pady=10)
        
        # Create notebook (tabbed interface)
        notebook = ttk.Notebook(frame)
        notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: List Vendors
        vendors_tab = ttk.Frame(notebook, padding=10)
        notebook.add(vendors_tab, text="List Vendors")
        
        # Create treeview for vendors
        columns = ('ID', 'Business Name', 'Feedback Score', 'Location')
        vendors_tree = ttk.Treeview(vendors_tab, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            vendors_tree.heading(col, text=col)
        
        vendors_tree.pack(fill='both', expand=True)
        
        def load_vendors():
            # Clear previous items
            for item in vendors_tree.get_children():
                vendors_tree.delete(item)
            
            vendors = self.platform.list_all_vendors()
            for vendor in vendors:
                vendors_tree.insert('', 'end', values=(
                    vendor['vendor_id'],
                    vendor['business_name'],
                    vendor['feedback_score'],
                    vendor['geographical_presence']
                ))
        
        def view_vendor_products():
            selected_item = vendors_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a vendor")
                return
            
            vendor_id = int(vendors_tree.item(selected_item, 'values')[0])
            products = self.platform.list_vendor_products(vendor_id)
            
            # Create a pop-up window with products
            products_window = tk.Toplevel(self.root)
            products_window.title("Vendor Products")
            products_window.geometry("700x400")
            
            vendor_name = vendors_tree.item(selected_item, 'values')[1]
            ttk.Label(products_window, text="{} Products".format(vendor_name), font=("Arial", 14)).pack(pady=10)
            
            # Create treeview for products
            columns = ('ID', 'Name', 'Price', 'Tag 1', 'Tag 2', 'Tag 3')
            products_tree = ttk.Treeview(products_window, columns=columns, show='headings')
            
            # Define headings
            for col in columns:
                products_tree.heading(col, text=col)
            
            products_tree.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Insert products
            for product in products:
                products_tree.insert('', 'end', values=(
                    product['product_id'],
                    product['name'],
                    "${:.2f}".format(product['price']),
                    product['tag1'] or "",
                    product['tag2'] or "",
                    product['tag3'] or ""
                ))
            
            ttk.Button(products_window, text="Close", command=products_window.destroy).pack(pady=10)
        
        vendors_button_frame = ttk.Frame(vendors_tab)
        vendors_button_frame.pack(fill='x', pady=10)
        
        ttk.Button(vendors_button_frame, text="Load Vendors", command=load_vendors).pack(side='left', padx=5)
        ttk.Button(vendors_button_frame, text="View Products", command=view_vendor_products).pack(side='left', padx=5)
        
        # Tab 2: Add Vendor
        add_vendor_tab = ttk.Frame(notebook, padding=10)
        notebook.add(add_vendor_tab, text="Add Vendor")
        
        ttk.Label(add_vendor_tab, text="Business Name:").pack(anchor='w')
        business_name_var = tk.StringVar()
        ttk.Entry(add_vendor_tab, textvariable=business_name_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(add_vendor_tab, text="Geographical Presence:").pack(anchor='w')
        location_var = tk.StringVar()
        ttk.Entry(add_vendor_tab, textvariable=location_var, width=40).pack(pady=5, fill='x')
        
        def submit_vendor():
            business_name = business_name_var.get()
            location = location_var.get()
            
            if business_name and location:
                vendor_id = self.platform.add_vendor(business_name, location)
                messagebox.showinfo("Success", "Vendor added successfully! Vendor ID: {}".format(vendor_id))
                business_name_var.set("")
                location_var.set("")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        ttk.Button(add_vendor_tab, text="Add Vendor", command=submit_vendor).pack(pady=10)
        
        # Tab 3: Add Product
        add_product_tab = ttk.Frame(notebook, padding=10)
        notebook.add(add_product_tab, text="Add Product")
        
        ttk.Label(add_product_tab, text="Vendor ID:").pack(anchor='w')
        vendor_id_var = tk.StringVar()
        ttk.Entry(add_product_tab, textvariable=vendor_id_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(add_product_tab, text="Product Name:").pack(anchor='w')
        product_name_var = tk.StringVar()
        ttk.Entry(add_product_tab, textvariable=product_name_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(add_product_tab, text="Price:").pack(anchor='w')
        price_var = tk.StringVar()
        ttk.Entry(add_product_tab, textvariable=price_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(add_product_tab, text="Tag 1:").pack(anchor='w')
        tag1_var = tk.StringVar()
        ttk.Entry(add_product_tab, textvariable=tag1_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(add_product_tab, text="Tag 2:").pack(anchor='w')
        tag2_var = tk.StringVar()
        ttk.Entry(add_product_tab, textvariable=tag2_var, width=40).pack(pady=5, fill='x')
        
        ttk.Label(add_product_tab, text="Tag 3:").pack(anchor='w')
        tag3_var = tk.StringVar()
        ttk.Entry(add_product_tab, textvariable=tag3_var, width=40).pack(pady=5, fill='x')
        
        def submit_product():
            try:
                vendor_id = int(vendor_id_var.get())
                name = product_name_var.get()
                price = float(price_var.get())
                tag1 = tag1_var.get() if tag1_var.get() else None
                tag2 = tag2_var.get() if tag2_var.get() else None
                tag3 = tag3_var.get() if tag3_var.get() else None
                
                if vendor_id and name and price:
                    product_id = self.platform.add_product(vendor_id, name, price, tag1, tag2, tag3)
                    messagebox.showinfo("Success", "Product added successfully! Product ID: {}".format(product_id))
                    product_name_var.set("")
                    price_var.set("")
                    tag1_var.set("")
                    tag2_var.set("")
                    tag3_var.set("")
                else:
                    messagebox.showerror("Error", "Vendor ID, name and price are required")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values")
        
        ttk.Button(add_product_tab, text="Add Product", command=submit_product).pack(pady=10)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill='x', pady=10)
        
        ttk.Button(bottom_frame, text="Back", command=self.setup_login_screen).pack(side='right')


if __name__ == "__main__":
    root = tk.Tk()
    app = EcommerceGUI(root)
    root.mainloop()