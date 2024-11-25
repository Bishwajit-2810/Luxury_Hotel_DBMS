import re
import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
import hashlib
import mysql.connector
import os  
from themes import apply_luxury_theme  


from modules.room_management import RoomManagement
from modules.booking_management import BookingManagement
from modules.payment_management import PaymentManagement
from modules.reports import Reports
from modules.guest_management import GuestManagement
from modules.service_management import ServiceManagement
from modules.feedback_management import FeedbackManagement



class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register - Luxury Hotel Management System")
        self.root.geometry("400x400")

        apply_luxury_theme(self.root)
        

        style = ttk.Style()
        style.configure("TEntry",
                        fieldbackground="#666666",  
                        foreground="white",          
                        font=("Arial", 14))         


        ttk.Label(self.root, text="Register", font=("Arial", 24, "bold"), foreground="#FFD700").pack(pady=20)

        # Username
        ttk.Label(self.root, text="Username:", font=("Arial", 14)).pack(pady=5)
        self.username_entry = ttk.Entry(self.root, style="TEntry")
        self.username_entry.pack(pady=5)

        # Password
        ttk.Label(self.root, text="Password:", font=("Arial", 14)).pack(pady=5)
        self.password_entry = ttk.Entry(self.root, style="TEntry", show="*")
        self.password_entry.pack(pady=5)

        # Confirm Password
        ttk.Label(self.root, text="Confirm Password:", font=("Arial", 14)).pack(pady=5)
        self.confirm_password_entry = ttk.Entry(self.root, style="TEntry", show="*")
        self.confirm_password_entry.pack(pady=5)

        ttk.Button(self.root, text="Register", command=self.register, style="Custom.TButton").pack(pady=20)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="LuxuryHotel"
            )
            cursor = connection.cursor()
            query = "INSERT INTO Users (Username, PasswordHash, Role, CreatedAt) VALUES (%s, %s, %s, NOW())"
            cursor.execute(query, (username, hashed_password, "User"))
            connection.commit()
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            self.root.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if connection:
                connection.close()


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Luxury Hotel Management System")
        self.root.geometry("400x400")

        apply_luxury_theme(self.root)
        

        style = ttk.Style()
        style.configure("TEntry",
                        fieldbackground="#666666",  
                        foreground="white",         
                        font=("Arial", 14))        


        ttk.Label(self.root, text="Login", font=("Arial", 24, "bold"), foreground="#FFD700").pack(pady=20)

        # Username
        ttk.Label(self.root, text="Username:", font=("Arial", 14)).pack(pady=5)
        self.username_entry = ttk.Entry(self.root, style="TEntry")
        self.username_entry.pack(pady=5)

        # Password
        ttk.Label(self.root, text="Password:", font=("Arial", 14)).pack(pady=5)
        self.password_entry = ttk.Entry(self.root, style="TEntry", show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self.root, text="Login", command=self.login, style="Custom.TButton").pack(pady=10)
        ttk.Button(self.root, text="Register", command=self.open_register_window, style="Custom.TButton").pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="LuxuryHotel"
            )
            cursor = connection.cursor()
            query = "SELECT * FROM Users WHERE Username=%s AND PasswordHash=%s"
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", "Login successful!")
                main_window = tk.Toplevel(self.root)
                self.root.withdraw()
                LuxuryHotelApp(main_window)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if connection:
                connection.close()

    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        RegisterWindow(register_window)



class LuxuryHotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Luxury Hotel Management System")
        self.root.geometry("1000x800") 
        apply_luxury_theme(root)  


        title_label = ttk.Label(
            self.root,
            text="Luxury Hotel Management System",
            font=("Georgia", 30, "bold"),
            foreground="#FFD700",
        )
        title_label.pack(pady=20)  

        # Frame to hold buttons and images
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20, expand=True)  


        self.room_img = self.resize_image("images/room_management_icon.png", 85, 80)
        self.booking_img = self.resize_image("images/booking_management_icon.png", 80, 80)
        self.payment_img = self.resize_image("images/payment_management_icon.png", 80, 80)
        self.report_img = self.resize_image("images/report_icon.png", 80, 80)
        self.guest_img = self.resize_image("images/guest_management_icon.png", 80, 80)
        self.service_img = self.resize_image("images/service_management_icon.png", 80, 80)
        self.feedback_img = self.resize_image("images/feedback_management_icon.png", 80, 80)


        button_width = 20 
        button_height = 3  


        ttk.Button(
            button_frame,
            text="Room Management",
            image=self.room_img,
            compound="left",  
            command=self.open_room_management,
            style="Custom.TButton",
            width=button_width,
            padding=10  # Space around text and image
        ).grid(row=0, column=0, padx=20, pady=20, sticky="ew")


        ttk.Button(
            button_frame,
            text="Booking Management",
            image=self.booking_img,
            compound="left",
            command=self.open_booking_management,
            style="Custom.TButton",
            width=button_width,
            padding=10
        ).grid(row=0, column=1, padx=20, pady=20, sticky="ew")


        ttk.Button(
            button_frame,
            text="Payment Management",
            image=self.payment_img,
            compound="left",
            command=self.open_payment_management,
            style="Custom.TButton",
            width=button_width,
            padding=10
        ).grid(row=1, column=0, padx=20, pady=20, sticky="ew")


        ttk.Button(
            button_frame,
            text="Guest Management",
            image=self.guest_img,
            compound="left",
            command=self.open_guest_management,
            style="Custom.TButton",
            width=button_width,
            padding=10
        ).grid(row=1, column=1, padx=20, pady=20, sticky="ew")


        ttk.Button(
            button_frame,
            text="Service Management",
            image=self.service_img,
            compound="left",
            command=self.open_service_management,
            style="Custom.TButton",
            width=button_width,
            padding=10
        ).grid(row=2, column=0, padx=20, pady=20, sticky="ew")


        ttk.Button(
            button_frame,
            text="Feedback Management",
            image=self.feedback_img,
            compound="left",
            command=self.open_feedback_management,
            style="Custom.TButton",
            width=button_width,
            padding=10
        ).grid(row=2, column=1, padx=20, pady=20, sticky="ew")


        ttk.Button(
            button_frame,
            text="Generate Reports",
            image=self.report_img,
            compound="left",
            command=self.open_reports,
            style="Custom.TButton",
            width=button_width,
            padding=10
        ).grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=2)


        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

    def resize_image(self, image_path, width, height):
        """Resize an image to the given width and height, with error handling."""
        if os.path.exists(image_path):
            image = PhotoImage(file=image_path)
            
            return image.subsample(int(image.width() / width), int(image.height() / height))
        else:
            print(f"Error: The image '{image_path}' was not found.")
            return None  
        
    def open_guest_management(self):
        GuestManagement(self.root)

    def open_room_management(self):
        RoomManagement(self.root)

    def open_booking_management(self):
        BookingManagement(self.root)

    def open_service_management(self):
        ServiceManagement(self.root)

    def open_feedback_management(self):
        FeedbackManagement(self.root)

    def open_payment_management(self):
        PaymentManagement(self.root)

    def open_reports(self):
        Reports(self.root)


def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    