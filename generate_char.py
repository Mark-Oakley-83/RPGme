import datetime
from char_gen_models import CreateCharacterSheet, convert_dumb_results, convert_dumb_weight_to_attributes
from new_char_interview import run_dumb_test

#TODO this file should contain the commands to create the character, just calling instructions

#Collect name and birthday
def gather_name_birthday():
    # Handles the initial name and birthday entry.
    print("--- Please Create A Character Sheet ---")
    name = input("Enter your name: ").strip()
    while True:
        try:
            date_str = input("Enter birthday (YYYY-MM-DD): ")
            birthday = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.date.today()
            age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            # return variables
            return name, birthday, age
        except ValueError:
            print("Format error. Please use YYYY-MM-DD (e.g., 1990-05-15).")


def gen_char_steps():
        #get name and birthday and age of player
    char_name, char_bday , char_age = gather_name_birthday()
        #create the player_char dictionary that will eventually be written to a file.
    player_char = CreateCharacterSheet(char_name, char_bday)
        #zodiac signs assignment handled by char_gen_models.CreateCharacterSheet
        #run the DUMB test and get the scores
    dumb_tally = run_dumb_test()
        #convert the talley to percentages
    dumb_weights = convert_dumb_results(dumb_tally)
        #declare and calculate the number of points
    char_att_points = (int(char_age) - 15) * .75
    char_skill_points = (int(char_age) - 15) * 3
    player_char.attributes = convert_dumb_weight_to_attributes(dumb_weights, char_att_points, player_char.attributes)


"""
#moon sign selection
#gather vocation information
#gather hobbies

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


