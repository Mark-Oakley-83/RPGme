#this is VERY much a work in progress and many of these files have not been created yet
#imports
from models import CreateCharacterSheet
from enter_name_birthday import gather_name_birthday


def main():
    # 1. Gather player name and birthday
    name, bday = gather_name_birthday()

    # 2. Initialize the permanent character object
    player_character = CreateCharacterSheet(name, bday)

    #this if else statement needs testing and a way to restart the character creation process
    if player_character.profile["zodiac"] == "Error: no Zodiac assigned":
        print("Error, please re-enter birthday, it did not register a Zodiac Sign.")
    #there may need to be other error messages later
    else:
        print(f"\nSuccessfully created: {player_character.profile['name']}")

"""
     3. Next run the interview portion
     interview_results = run_interview()
    4. Next run the vocation collector
     player_character.profile["active_vocation"] = initial_active_vocation_questions
     player_character.profile["retired_vocation"] = initial_retired_vocation_questions
    5. Run the Hobbies Questionaire
    6. Gather wieghts from the above functions
    active_vocation_weight = weigh_vocation(active, player_character.profile["active_vocation"])
    retired_vocation_weight = weigh_vocation(retired, player_character.profile["retired_vocation"])
    7. Apply weights to the points collected from age
     initial_attribute_points = age-15
     (age-15)*3=initial_skill_points
     player_character.apply_weights(results)
"""


if __name__ == "__main__":
    main()