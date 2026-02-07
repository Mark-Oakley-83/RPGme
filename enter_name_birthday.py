# enter_name_birthday.py
#this file prompts the user for their name and birthday.  This will be used to create the
#master character sheet and assign Zodiac sign and Age (for points totals upon finalization of
#initial creation)
import datetime

def gather_name_birthday():
    #Handles the initial name and birthday entry.
    print("--- Please Create A Character Sheet ---")
    name = input("Enter your name: ")

    while True:
        try:
            date_str = input("Enter birthday (YYYY-MM-DD): ")
            birthday = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            return name, birthday
        except ValueError:
            print("Format error. Please use YYYY-MM-DD (e.g., 1990-05-15).")

