import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import connect_to_db

class Reports:
    def __init__(self, root):

        self.window = tk.Toplevel(root)
        self.window.title("Generate Reports")
        self.window.geometry("800x600")
        self.window.configure(bg="#333333")  


        title_label = ttk.Label(
            self.window,
            text="Generate Reports",
            font=("Georgia", 24, "bold"),
            foreground="#FFD700",  
            background="#333333",
        )
        title_label.pack(pady=20)


        button_frame = ttk.Frame(self.window, padding="20 20 20 20", style="Dark.TFrame")
        button_frame.pack(pady=10)


        ttk.Button(button_frame, text="Guest Report", command=self.generate_guest_report, style="Luxury.TButton").grid(row=0, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Room Occupancy Report", command=self.generate_room_occupancy_report, style="Luxury.TButton").grid(row=1, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Revenue Report", command=self.generate_revenue_report, style="Luxury.TButton").grid(row=2, column=0, pady=10, padx=10)
        ttk.Button(button_frame, text="Service Usage Report", command=self.generate_service_report, style="Luxury.TButton").grid(row=3, column=0, pady=10, padx=10)


        style = ttk.Style()


        style.configure(
            "Luxury.TButton",
            font=("Arial", 12, "bold"),
            padding=10,
            foreground="#000000",  # Black text
            background="#FFD700",  # Gold background
            borderwidth=1,
        )
        style.map("Luxury.TButton", background=[("active", "#E6B800")])  


        style.configure("Dark.TFrame", background="#333333")

    def generate_guest_report(self):
        """Generate a report of all guests."""
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            query = "SELECT GuestID, Name, PhoneNumber, Email, Address FROM Guests"
            cursor.execute(query)
            guests = cursor.fetchall()

            self._display_report("Guest Report", guests, ["Guest ID", "Name", "Phone", "Email", "Address"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def generate_room_occupancy_report(self):
        """Generate a report of room occupancy status."""
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            query = """
                SELECT RoomNumber, RoomType, IsAvailable
                FROM Rooms
            """
            cursor.execute(query)
            rooms = cursor.fetchall()

            for i, room in enumerate(rooms):
                rooms[i] = list(room)
                rooms[i][2] = "Available" if room[2] else "Occupied"

            self._display_report("Room Occupancy Report", rooms, ["Room Number", "Room Type", "Status"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def generate_revenue_report(self):
        """Generate a report of total revenue from bookings and services."""
        conn = connect_to_db()
        cursor = conn.cursor()
        try:

            cursor.execute("SELECT SUM(TotalAmount) FROM Bookings")
            booking_revenue = cursor.fetchone()[0] or 0


            cursor.execute("SELECT SUM(ServiceCost) FROM Services")
            service_revenue = cursor.fetchone()[0] or 0


            total_revenue = booking_revenue + service_revenue

            report_data = [
                ["Total Booking Revenue", f"${booking_revenue:.2f}"],
                ["Total Service Revenue", f"${service_revenue:.2f}"],
                ["Total Revenue", f"${total_revenue:.2f}"],
            ]

            self._display_report("Revenue Report", report_data, ["Category", "Amount"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def generate_service_report(self):
        """Generate a report of service usage and revenue."""
        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            query = """
                SELECT BookingID, ServiceDescription, ServiceCost, ServiceDate
                FROM Services
            """
            cursor.execute(query)
            services = cursor.fetchall()

            self._display_report("Service Usage Report", services, ["Booking ID", "Service Description", "Service Cost", "Service Date"])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            conn.close()

    def _display_report(self, title, data, columns):
        """Display report in a new window using a treeview."""
        report_window = tk.Toplevel(self.window)
        report_window.title(title)
        report_window.geometry("800x400")
        report_window.configure(bg="#333333")


        tree = ttk.Treeview(report_window, columns=columns, show="headings", height=20)
        tree.pack(fill="both", expand=True)


        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=150)


        for row in data:
            tree.insert("", "end", values=row)


        y_scroll = ttk.Scrollbar(report_window, orient="vertical", command=tree.yview)
        y_scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=y_scroll.set)
