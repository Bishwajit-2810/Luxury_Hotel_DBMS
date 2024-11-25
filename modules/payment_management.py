import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db

class PaymentManagement:
    def __init__(self, root):

        self.window = tk.Toplevel(root)
        self.window.title("Manage Payments")
        self.window.geometry("800x600")
        self.window.configure(bg="#333333")  

        # Title label
        title_label = ttk.Label(
            self.window,
            text="Manage Payments",
            font=("Georgia", 24, "bold"),
            foreground="#FFD700",  
            background="#333333",
        )
        title_label.pack(pady=20)


        input_frame = ttk.Frame(self.window, padding="20 20 20 20", style="Dark.TFrame")
        input_frame.pack(pady=10, padx=20, fill="x", expand=True)


        ttk.Label(input_frame, text="Booking ID:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=0, column=0, sticky="w", pady=5)
        self.booking_id_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.booking_id_entry.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Amount Paid:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=1, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.amount_entry.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(input_frame, text="Payment Method:", font=("Arial", 12, "bold"), foreground="#FFFFFF").grid(row=2, column=0, sticky="w", pady=5)
        self.method_entry = ttk.Entry(input_frame, font=("Arial", 12), style="Custom.TEntry")
        self.method_entry.grid(row=2, column=1, pady=5, padx=10)


        button_frame = ttk.Frame(self.window, padding="10 10 10 10", style="Dark.TFrame")
        button_frame.pack(pady=20)


        add_button = ttk.Button(
            button_frame,
            text="Add Payment",
            command=self.add_payment,
            style="Luxury.TButton",
        )
        add_button.grid(row=0, column=0, padx=10)


        view_button = ttk.Button(
            button_frame,
            text="View Payments",
            command=self.view_payments,
            style="Luxury.TButton",
        )
        view_button.grid(row=0, column=1, padx=10)


        style = ttk.Style()


        style.configure(
            "Luxury.TButton",
            font=("Arial", 12, "bold"),
            padding=10,
            foreground="#000000", 
            background="#FFD700",  
            borderwidth=1,
        )
        style.map("Luxury.TButton", background=[("active", "#E6B800")]) 


        style.configure("Dark.TFrame", background="#333333")


        style.configure(
            "Custom.TEntry",
            fieldbackground="#666666",  
            foreground="#FFFFFF",  
            borderwidth=1,
        )

    def add_payment(self):
        """Add a payment to the database."""
        booking_id = self.booking_id_entry.get()
        amount = self.amount_entry.get()
        method = self.method_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        try:

            cursor.execute("SELECT BookingID FROM Bookings WHERE BookingID = %s", (booking_id,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Booking ID not found!")
                return


            query = "INSERT INTO Payments (BookingID, AmountPaid, PaymentMethod) VALUES (%s, %s, %s)"
            cursor.execute(query, (booking_id, amount, method))
            conn.commit()
            messagebox.showinfo("Success", "Payment added successfully!")
            self.clear_entries() 
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def view_payments(self):
        """View all payments."""
        conn = connect_to_db()
        cursor = conn.cursor()
        try:

            query = """
                SELECT p.PaymentID, p.BookingID, b.GuestID, p.AmountPaid, p.PaymentMethod, p.PaymentDate
                FROM Payments p
                INNER JOIN Bookings b ON p.BookingID = b.BookingID
            """
            cursor.execute(query)
            payments = cursor.fetchall()


            payment_window = tk.Toplevel(self.window)
            payment_window.title("All Payments")
            payment_window.geometry("600x400")
            payment_window.configure(bg="#333333")


            for i, payment in enumerate(payments, start=1):
                text = (
                    f"{i}. Payment ID: {payment[0]}, Booking ID: {payment[1]}, "
                    f"Guest ID: {payment[2]}, Amount: ${payment[3]}, "
                    f"Method: {payment[4]}, Date: {payment[5]}"
                )
                ttk.Label(
                    payment_window,
                    text=text,
                    foreground="#FFFFFF",
                    background="#333333",
                    font=("Arial", 11),
                ).pack(anchor="w", padx=20, pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def clear_entries(self):
        """Clear all input fields."""
        self.booking_id_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.method_entry.delete(0, tk.END)
