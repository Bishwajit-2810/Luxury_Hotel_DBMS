import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db

class BookingManagement:
    def __init__(self, root):

        self.window = tk.Toplevel(root)
        self.window.title("Manage Bookings")
        self.window.geometry("800x600")
        self.window.configure(bg="#333333")  


        title_label = ttk.Label(
            self.window,
            text="Manage Bookings",
            font=("Georgia", 24, "bold"),
            foreground="#FFD700",  
            background="#333333", 
        )
        title_label.pack(pady=20)  


        input_frame = ttk.Frame(self.window, padding="20 20 20 20", style="Dark.TFrame")
        input_frame.pack(pady=10, padx=20, fill="x", expand=True)


        ttk.Label(input_frame, text="Guest ID:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=0, column=0, sticky="w", pady=5)
        self.guest_id_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.guest_id_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Room ID:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=1, column=0, sticky="w", pady=5)
        self.room_id_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.room_id_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Check-In Date (YYYY-MM-DD):", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=2, column=0, sticky="w", pady=5)
        self.checkin_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.checkin_entry.grid(row=2, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Check-Out Date (YYYY-MM-DD):", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=3, column=0, sticky="w", pady=5)
        self.checkout_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.checkout_entry.grid(row=3, column=1, pady=5, padx=10)


        button_frame = ttk.Frame(self.window, padding="10 10 10 10", style="Dark.TFrame")
        button_frame.pack(pady=20)


        add_button = ttk.Button(
            button_frame,
            text="Add Booking",
            command=self.add_booking,
            style="Luxury.TButton"
        )
        add_button.grid(row=0, column=0, padx=10)


        style = ttk.Style()

        style.configure("Luxury.TButton",
                        font=("Arial", 12, "bold"),
                        padding=10,
                        foreground="#000000",  # Black text
                        background="#FFD700",  # Gold background
                        borderwidth=1)
        style.map("Luxury.TButton", background=[("active", "#E6B800")])  

        style.configure("Dark.TFrame", background="#333333") 


        style.configure("Custom.TEntry",
                        fieldbackground="#666666", 
                        foreground="#FFFFFF", 
                        borderwidth=1)

    def add_booking(self):
        """Add a new booking to the database."""
        guest_id = self.guest_id_entry.get()
        room_id = self.room_id_entry.get()
        check_in = self.checkin_entry.get()
        check_out = self.checkout_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:

            cursor.execute("SELECT PricePerNight FROM Rooms WHERE RoomID = %s", (room_id,))
            room = cursor.fetchone()
            if not room:
                messagebox.showerror("Error", "Room not found!")
                return

            price_per_night = room[0]
            query = """
            INSERT INTO Bookings (GuestID, RoomID, CheckInDate, CheckOutDate, TotalAmount) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (guest_id, room_id, check_in, check_out, price_per_night))
            conn.commit()
            messagebox.showinfo("Success", "Booking added successfully!")
            self.clear_entries() 
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def clear_entries(self):
        """Clear all input fields."""
        self.guest_id_entry.delete(0, tk.END)
        self.room_id_entry.delete(0, tk.END)
        self.checkin_entry.delete(0, tk.END)
        self.checkout_entry.delete(0, tk.END)
