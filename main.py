#this is VERY much a work in progress and many of these files have not been created yet
#input

from Models import CharacterSheet
from intake import gather_identity_data


def main():
    # 1. Gather initial data
    name, bday = gather_identity_data()

    # 2. Initialize the permanent character object
    player_character = CharacterSheet(name, bday)

    print(f"\nSuccessfully created: {player_character.profile['name']}")

    # 3. Next step will be:
    # results = run_interview()
    # player_character.apply_weights(results)


if __name__ == "__main__":
    main()