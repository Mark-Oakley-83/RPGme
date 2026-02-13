from pathlib import Path

def display_menu():
    #set the save file location and file type
    char_folder = Path("character_saves")
    char_file_extension = "*.json"

    #check to see if the folder and file are present first making a note that by default there are none
    has_char_sheet = False
    if char_folder.exists() and char_folder.is_dir():
        has_char_sheet = any(char_folder.glob(char_file_extension))

    # Format: "Display Name": "Internal Key"
    #This line is always present
    options = {"1": ("New Character", "new")}
#If the program finds a saved master sheet or snapshot sheets it will load this menu
    if has_char_sheet:
        options["2"] = ("Edit/update Snapshot", "edit_snap")
        options["3"] = ("Edit/update Master file", "edit_master")

    options["0"] = ("Exit", "exit")

    while True:
        print("\n--- MAIN MENU ---")
        for key, value in options.items():
            print(f"[{key}] {value[0]}")

        choice = input("\nSelect an option: ").strip()

        if choice in options:
            action = options[choice][1]

            if action == "new":
                print("Starting a new character...")
                return action
            elif action == "edit_snap":
                print("Loading your Snapshot list...")
                return action
            elif action == "edit_master":
                print("Loading your Master file list...")
                return action
            elif action == "exit":
                print("Goodbye!")
                break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    display_menu()