# intake.py
import datetime

def gather_identity_data():
    """Handles the initial name and birthday entry."""
    print("--- Character Identity Intake ---")
    name = input("Enter character name: ")

    while True:
        try:
            date_str = input("Enter birthday (YYYY-MM-DD): ")
            birthday = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            return name, birthday
        except ValueError:
            print("Format error. Please use YYYY-MM-DD (e.g., 1990-05-15).")