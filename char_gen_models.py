#AI Generated code to be verified
# char_gen_models.py
#TODO this code should only be for the backend steps for the character creation
import math
from assign_zodiac import get_zodiac_sign
from char_gen_vocations import vocation_questions
from data import TOTAL_PLAYER_INTERVIEW_HITS
from generate_char import gather_name_birthday, select_moon_sign, char_creation_hobbies
from new_char_interview import run_dumb_test


class CreateCharacterSheet:
    def __init__(self, name, birthday, age):
        self.profile = {
            "name": name,
            "birthday": birthday,
            "zodiac": get_zodiac_sign(birthday),  # Automatic assignment
            "age": age,
            "moon_sign": "",
            "active_vocations": [],
            "retired_vocations": [],  # New list for previous roles
            "hobbies": [],
            "foundation": None # e.g., "Academic", "Trade", or "Street"
        }
        #Base level Attributes for a basic nothing special sedentary office worker with no education
        self.attributes = {
            "Physical Pillar": {"Strength": 2, "Fortitude": 2, "Dexterity": 2},
            "Mental Pillar": {"Wisdom": 2, "Perception": 2, "Ingenuity": 2},
            "Social Pillar": {"Empathy": 2, "Composure": 2, "Conviction": 2},
            "Worldly Pillar": {"Aura": 2}
        }
        #List of universal skills set to 0 for base creation path
        self.skills = {
            "Instinct Pool": {"Alertness": 0, "Social Cues": 0, "Intuition": 0},
            "Training Pool": {"Coordination": 0, "Technique": 0, "Maintenance": 0},
            "Scholarship Pool": {"Research": 0, "Analysis": 0, "Instruction": 0}
        }

def gen_char_steps():
        # get name and birthday and age of player
    char_name, char_bday, char_age = gather_name_birthday()
        # create the player_char dictionary that will eventually be written to a file.
    player_char = CreateCharacterSheet(char_name, char_bday, char_age)
        # zodiac signs assignment handled by char_gen_models.CreateCharacterSheet
        # run the DUMB test and get the scores
    dumb_tally = run_dumb_test()
        # convert the talley to percentages
    dumb_weights = convert_dumb_results(dumb_tally)
        # declare and calculate the number of points
    char_att_points = int((int(char_age) - 15) * .75)
    #char_skill_points = (int(char_age) - 15) * 3
    player_char.attributes = convert_dumb_weight_to_attributes(dumb_weights, char_att_points)
    # allow the player to choose a moon sign
    player_char.profile["moon_sign"] = select_moon_sign()
    #begin vocation creation
    player_char.profile["active_vocations"] = vocation_questions(player_char.profile["active_vocations"], "active")
        #set up retired vocations
    player_char.profile["retired_vocations"] = vocation_questions(player_char.profile["retired_vocations"], "retired")
        #setup hobbies
    player_char.profile["hobbies"] = char_creation_hobbies(player_char.profile["hobbies"])

def add_vocation(vocation_list, new_vocation):
    """Adds a vocation only if the character has fewer than 3."""
    if len(vocation_list) < 3:
        vocation_list.append(new_vocation)
        return True
    else:
        return False

def retire_vocation(active_list, retired_list, vocation_name):
    if vocation_name in active_list:
        #Add to retired list
        retired_list.append(vocation_name)
        #Remove from active list
        active_list.remove(vocation_name)
        return active_list, retired_list
    else:
        return False

def remove_vocation(vocation_list, job_to_delete):
    if job_to_delete in vocation_list:
        vocation_list.remove(job_to_delete)
        return True
    else:
        return False

def convert_dumb_results(results):
    #converts weights from numbers to percentages
    dumb_percents = {key: (value / TOTAL_PLAYER_INTERVIEW_HITS) * 100 for key, value in results.items()}
    return dumb_percents

def convert_dumb_weight_to_attributes(weights, avail_points):
    #converts the weights from the above function to actual points
    #declare variables
    assigned_points = {}
    remainders = {}
    total_assigned = 0
    #while there is an attribute to adjust, run each in order
    for attr, weight in weights.items():
        exact_value = (weight / 100) * avail_points
        if exact_value > 8:
           exact_value = 8
        assigned_points[attr] = math.floor(exact_value)
        remainders[attr] = exact_value - assigned_points[attr]
        total_assigned += assigned_points[attr]
    #set the leftovers for remainder assignment
    leftover = avail_points - total_assigned
    #sort the remainders highest to lowest
    sorted_by_remainder = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
    #run this for each point left over until all points are used
    for i in range(leftover):
        attr_to_boost = sorted_by_remainder[i][0]
        assigned_points[attr_to_boost] += 1
#TODO think about making these points leveled: first point = 1xp, second point =2xp etc
    return assigned_points

def standardize_hobby(name, skills, last_used, years_used):
    #standarize the hobby entries
    return {
        "name": name,
        "skills": skills,  # Expecting a list like ["Electronics", "Math"]
        "last_used": int(last_used),
        "years_active": int(years_used)
    }


"""
#todo

    def add_hobby(self, new_hobby):
        self.profile["hobbies"].append(new_hobby)


Needs:
add_retired_initial #adds inital retired vocations without the check to see if they were already active
initial_active_vocation_questions #separate file?
initial_retired_vocation_questions #separate file?
create_custom_vocation_tool
??export_customizations_to_email?
append_vocation
remove_hobby
add_certification
remove_certification
calc_vocation_depreciation
apply_attribute_weights(total_creation_attribute_points)
create_custom_skills_tool
append_skills_list
apply_points_from_vocations
generate_printable_character_sheet
snapshot_creation
"""