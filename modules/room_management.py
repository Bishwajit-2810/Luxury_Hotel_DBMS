import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db

class RoomManagement:
    def __init__(self, root):

        self.window = tk.Toplevel(root)
        self.window.title("Room Management")
        self.window.geometry("800x600")
        self.window.configure(bg="#333333")  


        title_label = ttk.Label(
            self.window,
            text="Manage Rooms",
            font=("Georgia", 24, "bold"),
            foreground="#FFD700",  
            background="#333333",  
        )
        title_label.pack(pady=20)  


        input_frame = ttk.Frame(self.window, padding="20 20 20 20", style="Dark.TFrame")
        input_frame.pack(pady=10, padx=20, fill="x", expand=True)


        ttk.Label(input_frame, text="Room Number:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=0, column=0, sticky="w", pady=5)
        self.room_number_entry = ttk.Entry(input_frame, font=("Arial", 14), style="Custom.TEntry", width=40)  # Larger text field
        self.room_number_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Room Type:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=1, column=0, sticky="w", pady=5)
        self.room_type_entry = ttk.Entry(input_frame, font=("Arial", 14), style="Custom.TEntry", width=40)  # Larger text field
        self.room_type_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Price Per Night ($):", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=2, column=0, sticky="w", pady=5)
        self.price_entry = ttk.Entry(input_frame, font=("Arial", 14), style="Custom.TEntry", width=40)  # Larger text field
        self.price_entry.grid(row=2, column=1, pady=5, padx=10)


        button_frame = ttk.Frame(self.window, padding="10 10 10 10", style="Dark.TFrame")
        button_frame.pack(pady=20)


        add_button = ttk.Button(
            button_frame,
            text="Add Room",
            command=self.add_room,
            style="Luxury.TButton"
        )
        add_button.grid(row=0, column=0, padx=10)

        view_button = ttk.Button(
            button_frame,
            text="View All Rooms",
            command=self.view_rooms,
            style="Luxury.TButton"
        )
        view_button.grid(row=0, column=1, padx=10)


        style = ttk.Style()

        style.configure("Luxury.TButton",
                        font=("Arial", 12, "bold"),
                        padding=10,
                        borderwidth=1)
        style.map("Luxury.TButton", background=[("active", "#E6B800")])  


        style.configure("Dark.TFrame", background="#333333") 
        

        style.configure("Custom.TEntry",
                        borderwidth=1)  

    def add_room(self):
        """Add a new room to the database."""
        room_number = self.room_number_entry.get()
        room_type = self.room_type_entry.get()
        price = self.price_entry.get()

        if not room_number or not room_type or not price:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price per night must be a valid number!")
            return

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO Rooms (RoomNumber, RoomType, PricePerNight) VALUES (%s, %s, %s)"
            cursor.execute(query, (room_number, room_type, price))
            conn.commit()
            messagebox.showinfo("Success", "Room added successfully!")
            self.clear_entries()  
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def view_rooms(self):
        """Display all rooms in a new window."""
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM Rooms"
            cursor.execute(query)
            rooms = cursor.fetchall()


            room_window = tk.Toplevel(self.window)
            room_window.title("All Rooms")
            room_window.geometry("600x400")
            room_window.configure(bg="#333333")  


            tree_frame = ttk.Frame(room_window, padding="10 10 10 10", style="Dark.TFrame")
            tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

            columns = ("Room Number", "Room Type", "Price Per Night")
            room_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
            room_tree.pack(fill="both", expand=True)


            for col in columns:
                room_tree.heading(col, text=col, anchor="center")
                room_tree.column(col, anchor="center", width=150)


            for room in rooms:
                room_tree.insert("", "end", values=(room[1], room[2], f"${room[3]}"))


            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=room_tree.yview)
            room_tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def clear_entries(self):
        """Clear all input fields."""
        self.room_number_entry.delete(0, tk.END)
        self.room_type_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
