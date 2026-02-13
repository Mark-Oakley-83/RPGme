from enter_name_birthday import gather_name_birthday
from new_char_interview import run_dumb_test

#Collect name and birthday
char_name, char_bday = gather_name_birthday()
#run the DUMB test and get the scores
dumb_tally = run_dumb_test()
"""
#zodiac signs assignment
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


