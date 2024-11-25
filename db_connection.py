import mysql.connector

def connect_to_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="LuxuryHotel"
    )
