import datetime
import csv

from char_gen_models import standardize_hobby


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

def select_moon_sign():
    menu_header = """
    -----------------------Here are a selection of moon signs-----------------------
    (Please pick the one that aligns most with your personality, or not... whatevs):
    --------------------------------------------------------------------------------
    
    """
    print (menu_header)
    #create a local memory list of moon signs
    with open('moon_phases.csv', mode='r', encoding='utf-8') as file:
        moon_data = list(csv.DictReader(file))
    #print the menu with a number, name, and fancy description
    for row in moon_data:
        print(row['id'], row['phase_name'], "-", row['description'])
    while True:
        #get the user input
        moon_sign_selection = input("Please select your moon sign: ").strip()
        #Search the list for the matching ID
        for row in moon_data:
            if row['id'] == moon_sign_selection:
                return row['phase_name']  # Success! Return the name, not the ID
        print("Invalid selection. Please enter a number from the list.")

def char_creation_hobbies(hobbies_list):
    print("""
          So let's get to know you better, because we haven't done enough of that yet... 
          What kind of things do you do that we can list as hobbies?
          For these next questions keep in mind the standard skills are:
          --Alertness       Social Cues     Intuition
          --Coordination    Technique       Maintenance
          --Research        Analysis        Instruction
          But for this section, you can add custom ones.  Just be aware that they should 
          be specific and will take away from points in the main skills later.
          """)
    another_hobby = "Y"
    while another_hobby == "Y":
        name = input("Please enter a hobby: ")
        raw_skills = input("Please enter up to 3 skills you use with this hobby: (Separate them with commas Alertness,Research,...): ")
            # set the skills to Title case, strips extra spaces at the beginning and end of each skill, and removed empty skills
        clean_skills = [skill.strip().title() for skill in raw_skills.split(",") if skill.strip()]
        last_used = input("When did you last enjoy this hobby (just enter the 4 digit year: ")
        years_active = input("How many years have you been enjoying this hobby? (enter a number) ")
        new_hobby = standardize_hobby(name, clean_skills, last_used, years_active)
        hobbies_list.append(new_hobby)
        another_hobby = input("Would you like to add another hobby? Y/N ").upper()





"""

    4. Next run the vocation collector
     player_character.profile["active_vocation"] = initial_active_vocation_questions
     player_character.profile["retired_vocation"] = initial_retired_vocation_questions
    5. Run the Hobbies Questionaire
    6. Gather wieghts from the above functions
    active_vocation_weight = weigh_vocation(active, player_character.profile["active_vocation"])
    retired_vocation_weight = weigh_vocation(retired, player_character.profile["retired_vocation"])
    7. Apply weights to the points collected from age
     
     player_character.apply_weights(results)
"""


