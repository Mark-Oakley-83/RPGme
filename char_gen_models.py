#AI Generated code to be verified
# char_gen_models.py
#TODO this code should only be for the backend steps for the character creation
import math

from pycparser.c_ast import Return

from assign_zodiac import get_zodiac_sign
from data import TOTAL_PLAYER_INTERVIEW_HITS


class CreateCharacterSheet:
    def __init__(self, name, birthday):
        self.profile = {
            "name": name,
            "birthday": birthday,
            "zodiac": get_zodiac_sign(birthday),  # Automatic assignment
            #"age": age_calculation
            "active_vocation": [],
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
        self.active_vocation = []
        self.retired_vocations = []
        self.hobbies = []



def add_vocation(char_obj, new_vocation):
    """Adds a vocation only if the character has fewer than 3."""
    if len(char_obj.profile["active_vocations"]) < 3:
        char_obj.profile["active_vocations"].append(new_vocation)
    else:
        print("Maximum active vocations (3) reached.")

def retire_vocation(char_obj, vocation_name):
    if vocation_name in char_obj.profile["active_vocations"]:
        # 2. Add to retired list
        char_obj.profile["retired_vocations"].append(vocation_name)
        # 1. Remove from active list
        char_obj.profile["active_vocations"].remove(vocation_name)
        print(f"{vocation_name} has been retired.")
    else:
        print(f"Error: {vocation_name} is not currently an active vocation.")

def convert_dumb_results(results):
    #converts weights from numbers to percentages
    dumb_percents = {key: (value / TOTAL_PLAYER_INTERVIEW_HITS) * 100 for key, value in results.items()}
    Return (dumb_percents)

def convert_dumb_weight_to_attributes(weights, avail_points, start_attribs):
    #converts the weights from the above function to actual points
    #declare variables
    assigned_points = {}
    remainders = {}
    total_assigned = 0
    for attr, weight in weights.items():
        exact_value = (weight / 100) * avail_points
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
    #TODO make a soft cap of 8 and redistribure those points
    #TODO make these points leveled first point = 1xp, second point =2xp etc

    return assigned_points


#todo
"""
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