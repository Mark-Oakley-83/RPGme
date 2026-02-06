#AI generated code to be reviewed and verified before use
import datetime

class CharacterSheet:
    def __init__(self, name, birthday):
        self.profile = {
            "name": name,
            "birthday": birthday,  # Stored as a datetime object
            "vocation": None,
            "hobbies": []
        }
        
        # Initializing Pillars with 0 for now (to be filled by the Interview)
        self.attributes = {
            "Physical Pillar": {"Strength": 0, "Fortitude": 0, "Dexterity": 0},
            "Mental Pillar": {"Wisdom": 0, "Perception": 0, "Ingenuity": 0},
            "Social Pillar": {"Emotional Intelligence": 0, "Composure": 0, "Conviction": 0},
            "Worldly Pillar": {"Aura": 0}
        }

def get_birthday():
    """Prompts the user for birthday components and returns a datetime object."""
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
    character = CharacterSheet(player_name, player_birthday)

    print(f"\nCharacter '{character.profile['name']}' initialized.")
    print(f"Recorded Birthday: {character.profile['birthday']}")
    print("System ready for Stage 3: The 20-Question Interview.")
    
    # Future hook for the Interview module:
    # run_interview(character)

if __name__ == "__main__":
    main()
