#this is VERY much a work in progress and many of these files have not been created yet

#Welcome message
print("Hello, welcome to RPGme.  Let me boot up quick...")
#imports
from models import CreateCharacterSheet
from enter_name_birthday import gather_name_birthday
from main_menu import display_menu


def main():
    #Launch main menu
    action = display_menu()
    if action == "new": #launch character creation process
        player_character = generate_char()

        #this if else statement needs testing and a way to restart the character creation process
        if player_character.profile["zodiac"] == "Error: no Zodiac assigned":
            print("Error, please re-enter birthday, it did not register a Zodiac Sign.")
        #elif----there may need to be other error messages later
        else:
            print(f"\nSuccessfully created: {player_character.profile['name']}")




if __name__ == "__main__":
    main()