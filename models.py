#AI Generated code to be verified
# models.py
from assign_zodiac import get_zodiac_sign

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
            "Social Pillar": {"Emotional Intelligence": 2, "Composure": 2, "Conviction": 2},
            "Worldly Pillar": {"Aura": 2}
        }
        #List of universal skills set to 0 for base creation path
        self.skills = {
            "Instinct Pool": {"Alertness": 0, "Social Cues": 0, "Intuition": 0},
            "Training Pool": {"Coordination": 0, "Technique": 0, "Maintenance": 0},
            "Scholarship Pool": {"Research": 0, "Analysis": 0, "Instruction": 0}
        }

    def add_vocation(self, new_vocation):
        """Adds a vocation only if the character has fewer than 3."""
        if len(self.profile["active_vocations"]) < 3:
            self.profile["active_vocations"].append(new_vocation)
        else:
            print("Maximum active vocations (3) reached.")

    def retire_vocation(self, vocation_name):
        if vocation_name in self.profile["active_vocations"]:
            # 2. Add to retired list
            self.profile["retired_vocations"].append(vocation_name)
            # 1. Remove from active list
            self.profile["active_vocations"].remove(vocation_name)
            print(f"{vocation_name} has been retired.")
        else:
            print(f"Error: {vocation_name} is not currently an active vocation.")
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
questionare #separate file!!!
apply_attribute_weights(total_creation_attribute_points)
create_custom_skills_tool
append_skills_list
apply_points_from_vocations
generate_printable_character_sheet
snapshot_creation
"""