import datetime
import csv


from char_gen_models import standardize_hobby

# this file should contain the commands to create the character, just calling instructions

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

def char_creation_hobbies(hobbies_list, universal_skills, hobby_skills):
    print("""
          So let's get to know you better, because we haven't done enough of that yet... 
          What kind of things do you do that we can list as hobbies?
          For these next questions keep in mind the standard skills are:
          --Alertness       Social Cues     Intuition
          --Coordination    Technique       Maintenance
          --Research        Analysis        Instruction
          But for this section, you can add custom ones.  Just be aware that they should 
          be specific, will need to select a pool to draw from, and will take away from 
          points in the main skills later.
          """)
    another_hobby = "Y"
    while another_hobby == "Y":
        name = input("Please enter a hobby: (i.e. kayaking, 3D printing, electronics repair) ") #ask for a hobby name
        raw_skills = input("Please enter up to 3 skills you use with this hobby: (Separate them with commas Alertness,Research,...): ") #ask for a set of skills
            # set the skills to Title case, strips extra spaces at the beginning and end of each skill, and removed empty skills
        clean_skills = [skill.strip().title() for skill in raw_skills.split(",") if skill.strip()]
        all_known_skills = set() #initialize a set to put all known skills into
        for pool_name in universal_skills: #run this for each item in the list (this is repeated after each skill is added to prevent duplication)
            all_known_skills.update(pool_name.keys())
        for pool_name in hobby_skills:
            all_known_skills.update(pool_name.keys())
        for skill in clean_skills: #if the skill is in the skills list already...
            if skill in all_known_skills:
            # It's already there (Universal or previously added Custom)
                continue
            else: #if it's not already in the list
                pool_map = {"1": "Instinct Pool", "2": "Training Pool", "3": "Scholarship Pool"}
                print(f"""We need to assign {skill} to a pool for your skills, there are 3 options.
                Instinct Skills are innate.  They are things most of us take for granted like: alertness, social clues, and intuition.
                Training Skills are hands-on.  They are things that are trained like: coordination, technique, and maintenance.
                Scholarship skills are academic.  They are things that relate to cerebral leaning like: research, analysis, and instruction.
                1: Instinct, 2: Training, 3: Scholarship
                """)
                choice = input(f"Which pool does '{skill}' belong to? ")
                target_pool = pool_map.get(choice)
                if target_pool:
                    if max_skills_check(hobby_skills, target_pool):
                        hobby_skills[target_pool][skill] = 0
                    else:
                        print("Sorry that skill was not added.")
                        continue
        last_used = input("When did you last enjoy this hobby (just enter the 4 digit year: ")
        years_active = input("How many years have you been enjoying this hobby? (enter a number) ")
        new_hobby = standardize_hobby(name, clean_skills, last_used, years_active)
        hobbies_list.append(new_hobby)
        another_hobby = input("Would you like to add another hobby? Y/N ").upper()

def char_creation_foundation(foundation):
    print("""
    Quick question: How did you grow up?
    1) I went to high school, then went off to college, and have (or will have) a degree and nice job.
    2) I did ok in high school, or dropped out, then got a technical certification and went to work.
    3) I did the whole high school thing (or didn't) and decided to learn my trade through grit and experience.
    4) I joined the military at a early age and got my training and experience from that.
    If none of these fit you, just pick the one that's most like your life currently.
    """)
    choice = input("Which of these fits you best? (please enter 1,2, 3, or 4)")
    if choice == "1":
        foundation = "Academic"
    if choice == "2":
        foundation = "Trade"
    if choice == "3":
        foundation = "Street"
    if choice == "4":
        foundation = "Military"
    return foundation

def max_skills_check(hobby_skills, target_pool):
    #create a list of the skills in that pool
    hobby_target_pool = hobby_skills[target_pool]
    # check to see if player_skill[pool] is full
    if len(hobby_target_pool) < 3:
        # if it is not, return true
        return True
    print("Sorry that pool is full, would you like to remove an old skill?\n")
    while True:
        #get the current list of skills in that skill pool
        skills_list = list(hobby_target_pool.keys())
        #print the skills list
        for index, skill_name in enumerate(skills_list, start=1):
            print(f"{index}: {skill_name}")
        # ask which one to remove or to ignore the new skill
        choice_old_skill = input ("Enter the number 0 to not add the new skill, or enter the number of the old skill to remove")
        if choice_old_skill == "0":     #if they choose not to add the new skill, return false
            return False
        # if they choose to remove an old skill
        if choice_old_skill.isdigit():
            int_old_skill = int(choice_old_skill) - 1
            # Check if the number is within the valid range of the list
            if 0 <= int_old_skill < len(skills_list):
                selected_skill = skills_list[int_old_skill]
                confirm_choice = input(f"Please confirm {selected_skill} is to be removed. Y/N : ").upper()
                if confirm_choice == "Y":
                    hobby_target_pool.pop(selected_skill)
                    print(f"Removed {selected_skill}.")
                    return True
                elif confirm_choice == "N":
                    print("\nLet's try that again...")
                    continue
            else:
                print("Invalid number. Please pick a number from the list.")
        else:
            print("Please enter a numeric value.")







    #return true
    #actual addition takes place in called script
"""

    Gather weights in models file from the above functions
    active_vocation_weight = weigh_vocation(active, player_character.profile["active_vocation"])
    retired_vocation_weight = weigh_vocation(retired, player_character.profile["retired_vocation"])
    7. Apply weights to the points collected from age
     
     player_character.apply_weights(results)
"""


