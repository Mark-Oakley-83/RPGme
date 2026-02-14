#AI generated code to be reviewed and verified before use
import datetime
import char_gen_models

def get_birthday():
    #Prompts the user for birthday components and returns a datetime object.
    while True:
        try:
            year = int(input("Enter birth year (YYYY): "))
            month = int(input("Enter birth month (MM): "))
            day = int(input("Enter birth day (DD): "))
            return datetime.date(year, month, day)
        except ValueError:
            print("Invalid date. Please enter numerical values (e.g., 1983, 05, 12).")

def main():
    print("--- RPG System Character Initialization ---")
    
    # Step 1: Identity Intake
    player_name = input("Enter your character's name: ")
    player_birthday = get_birthday()

    # Step 2: Initialize Permanent Object
    character = models.CreateCharacterSheet(player_name, player_birthday)

    print(f"\nCharacter '{character.profile['name']}' initialized.")
    print(f"Recorded Birthday: {character.profile['birthday']}")
    print("System ready for Stage 3: The 20-Question Interview.")
    
    # Future hook for the Interview module:
    # run_interview(character)

if __name__ == "__main__":
    main()
