#this is VERY much a work in progress and many of these files have not been created yet
from generate_char import gen_char_steps

#Welcome message
print("Hello, welcome to RPGme.  Let me boot up quick...")
#imports
from generate_char import gen_char_steps
from main_menu import display_menu

def main():
    #Launch main menu
    action = display_menu()
    if action == "new": #launch character creation process

        player_character = gen_char_steps()

        print(f"\nSuccessfully created: {player_character.profile['name']}")




if __name__ == "__main__":
    main()