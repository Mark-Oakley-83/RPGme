# char_gen_models.py
#this code should only be for the backend steps for the character creation
import math
import datetime

from char_creation_skills_models import skill_weight_calc
from char_gen_vocations import vocation_questions
from data import TOTAL_PLAYER_INTERVIEW_HITS
from generate_char import gather_name_birthday, select_moon_sign, char_creation_hobbies, char_creation_foundation, \
    zodiac_moon_att_adjustments
from new_char_interview import run_dumb_test
import pandas as pd

def get_zodiac_sign(birthday):
    """Calculates the Zodiac sign based on a datetime.date object."""
    month = birthday.month
    day = birthday.day

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    elif (month == 2 and day >= 19) or (month == 3 and day <=20):
        return "Pisces"
    #covers all signs, so that if there is an error with the birthday, an error is
    #returned and can be dealt with
    else:
        return "Error: no Zodiac assigned"

class CreateCharacterSheet:
    def __init__(self, name, birthday, age):
        birthday = pd.to_datetime(birthday)
        self.profile = {
            "name": name,
            "birthday": birthday,
            "zodiac": get_zodiac_sign(birthday),  # Automatic assignment
            "age": age,
            "moon_sign": "",
            "active_vocations": [],
            "retired_vocations": [],  # New list for previous roles
            "hobbies": [],
            "foundation": "" # e.g., "Academic", "Trade", or "Street"
        }
        #Base level Attributes for a basic nothing special sedentary office worker with no education
        self.attributes = {
            "Physical Pillar": {"Strength": 2, "Fortitude": 2, "Dexterity": 2},
            "Mental Pillar": {"Wisdom": 2, "Perception": 2, "Ingenuity": 2},
            "Social Pillar": {"Empathy": 2, "Composure": 2, "Conviction": 2},
            "Worldly Pillar": {"Aura": 2}
        }
        #List of universal skills set to 0 for base creation path
        self.universal_skills = {
            "Instinct Pool": {
                "Alertness": {"level": 0, "pillar": "physical","Journeyman_lock": False},
                "Social Cues": {"level": 0, "pillar": "social","Journeyman_lock": False},
                "Intuition": {"level": 0, "pillar": "mental","Journeyman_lock": False}
            },
            "Training Pool": {
                "Coordination": {"level": 0, "pillar": "physical","Journeyman_lock": False},
                "Technique": {"level": 0, "pillar": "social","Journeyman_lock": False},
                "Maintenance": {"level": 0, "pillar": "mental","Journeyman_lock": False},
            },
            "Scholarship Pool":{
                 "Research": {"level": 0, "pillar": "physical","Journeyman_lock": False},
                 "Analysis": {"level": 0, "pillar": "social","Journeyman_lock": False},
                 "Instruction": {"level": 0, "pillar": "mental","Journeyman_lock": False}
                 }
        }
        self.voc_skills ={
            "Instinct Pool": {},
            "Training Pool": {},
            "Scholarship Pool": {}
        }
        self.hobby_skills = {
            "Instinct Pool": {},
            "Training Pool": {},
            "Scholarship Pool": {}
        }
        self.skill_master = {}

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
    player_char.attributes = convert_dumb_weight_to_attributes(dumb_weights, char_att_points, player_char.attributes)
    # allow the player to choose a moon sign
    player_char.profile["moon_sign"] = select_moon_sign()
    zodiac_moon_att_adjustments(player_char.attributes, player_char.profile["zodiac"], player_char.profile["moon_sign"])
    #begin vocation creation
    player_char.profile["active_vocations"] = vocation_questions(player_char.profile["active_vocations"], "active", player_char.voc_skills)
        #set up retired vocations
    player_char.profile["retired_vocations"] = vocation_questions(player_char.profile["retired_vocations"], "retired", player_char.voc_skills)
        #setup hobbies
    player_char.profile["hobbies"] = char_creation_hobbies(player_char.profile["hobbies"], player_char.universal_skills, player_char.hobby_skills, player_char.voc_skills)
        #determine how the player lived his life e.g., "Academic", "Trade", or "Street"
    player_char.profile["foundation"] = char_creation_foundation(player_char.profile["foundation"])
    #Special bonus for military members
    if player_char.profile["foundation"] == "Military":
        player_char.attributes["Worldly Pillar"]["Aura"] += 1
        #determine skill weights
    skill_weight_calc(player_char)

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

def convert_dumb_weight_to_attributes(weights, avail_points, current_attr):
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
    for pillar , attrs in current_attr.items():
        for attr_name in attrs:
            if attr_name in assigned_points:
                current_attr[pillar][attr_name] = assigned_points[attr_name]

    return current_attr

def standardize_hobby(name, skills, last_used, years_used):
    #standarize the hobby entries
    return {
        "name": name,
        "skills": skills,  # Expecting a list like ["Electronics", "Math"]
        "last_used": int(last_used),
        "years_active": int(years_used),

    }


"""
todo

Needs:
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