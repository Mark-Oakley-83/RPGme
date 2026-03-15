import csv
import data


def get_data_by_level(filename, level_column, prefix):
    items = []
    with open(filename, mode='r', encoding='utf-8-sig', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row[level_column]
            # Check if this row is the level we want and matches our prefix
            if code and code.startswith(prefix):
                items.append({'code': code, 'name': row['Name']})
    return items


def vocation_questions(player_vocations, voc_type, voc_skills):
    #get the voc_type and present the player with 2 greetings
    num_jobs = 0
    tenure = 0
    #greet the player and explain 3 jobs and the SOC list
    if voc_type == "active":
        print(f"""
        
            Let's set up your jobs and descriptions...
        
            We are setting the limit for active vocations to 3, if you have more than that
            we can add them as hobbies later.
        
            This will determine your starting skills and other features.
        
            Since there are so many job descriptions available, we will use the government's choices.
            Because we all know the government is paid to be efficient and accurate.
            
            If you have a very very unusual job, we can deal with that in another step, for now....
            """)
        num_jobs = int(input("\nHow many jobs do you have? Enter 1,2, or 3: "))
    elif voc_type == "retired":
            print(f"""
    Let's set up your old jobs and descriptions...
    
    These will give you credit for jobs you have done in the past.
    
    Since there are so many job descriptions available, we will use the government's choices.
    Because we all know the government is paid to be efficient and accurate.
    
    If you have a very very unusual job, we can deal with that in another step, for now....
    """)
            num_jobs = int(input("\nHow many jobs have you had in the past? Enter a number: "))
    # if voc_type is active, get no more than 3 jobs
    if voc_type == "active" and num_jobs > 3:
            print("Sorry, we can only handle 3 jobs at a time. We can add the others as hobbies later.")
            num_jobs = 3
    #if voc_type is retired, as many as you want
    elif voc_type == "retired" or num_jobs < 3:
            print("Ok, lets get started")
    # for as many times as voc type allows
    while num_jobs > 0:
        #Entering the menu
        job_name, job_age = vocation_menu(voc_type)
        #if the job was short
        if job_age <= 1 and voc_type == "active":
            under_6 = input(f"Was {job_name} less than 6 months (doesn't have to be exact)? Y/N: ").upper()
            if under_6 == "Y":
                job_age = 0
            elif under_6 == "N":
                job_age = 1
        if voc_type == "retired":
            tenure = int(input(f"How many years were you a {job_name} (enter a number):"))
            player_vocations.append({'name': job_name, 'age':job_age, 'tenure': tenure})
        else:
            #append the player sheet
            player_vocations.append({'name': job_name, 'age': job_age})

        #reduce the num of jobs to be added
        num_jobs -= 1
    else:
        print(f"These are now your {voc_type} vocations!\n")
        print(f"{player_vocations} \n")
        if voc_type == 'active':
            for entry in player_vocations:
                if entry['age'] >= 11:
                    target_pool, clean_skills, target_pillar = add_custom_vocation_skill(entry['name'], 'Journeyman')
                    voc_skills[target_pool][clean_skills] = {"level": 0, "pillar": target_pillar, "length_since": 0, "length_in": entry['age'],"Journeyman_lock": True}
                if entry['age'] >= 16:
                    target_pool, clean_skills, target_pillar = add_custom_vocation_skill(entry['name'], 'Expert')
                    voc_skills[target_pool][clean_skills] =  {"level": 0, "pillar": target_pillar, "length_since": 0, "length_in": entry['age'],"Journeyman_lock": True}
        if voc_type == 'retired':
            for entry in player_vocations:
                if tenure >= 11:
                    target_pool, clean_skills, target_pillar = add_custom_vocation_skill(entry['name'], 'Journeyman')
                    voc_skills[target_pool][clean_skills] = {"level": 0, "pillar": target_pillar, "length_in": entry['tenure'], "length_since": entry['age'],"Journeyman_lock": True}
                if tenure >= 16:
                    target_pool, clean_skills, target_pillar = add_custom_vocation_skill(entry['name'], 'Expert')
                    voc_skills[target_pool][clean_skills] =  {"level": 0, "pillar": target_pillar, "length_in": entry['tenure'], "length_since": entry['age'],"Journeyman_lock": True}

    return player_vocations

def add_custom_vocation_skill(name, level):
    print(f"Your years as a/an \"{name}\" Qualifies you as a/an \"{level}\" in the field.\n Please enter a custom skill you would like to add that is associated with this job.\n")
    raw_skills = input("Just one, anything you like, 2-3 words no commas: ")  # ask for a skill
    # set the skills to Title case, strips extra spaces at the beginning and end of each skill, and removed empty skills
    clean_skills = raw_skills.split(",")[0].strip().title()
    pool_map = {"1": "Instinct Pool", "2": "Training Pool", "3": "Scholarship Pool"}
    print(f"""We need to assign {clean_skills} to a pool for your skills, there are 3 options.
    
    1) Instinct Skills are innate.  They are things most of us take for granted like: alertness, social clues, and intuition.
    2) Training Skills are hands-on.  They are things that are trained like: coordination, technique, and maintenance.
    3) Scholarship skills are academic.  They are things that relate to cerebral leaning like: research, analysis, and instruction.
    
    Please select 1: Instinct, 2: Training, 3: Scholarship
    """)
    choice = input(f"Which pool does '{clean_skills}' belong to? 1, 2, or 3: ")
    target_pool = pool_map.get(choice)
    pillar_map = {"1": "Physical", "2": "Mental", "3": "Social"}
    print(f"""We need to assign {clean_skills} to a Attribute Pillar too, there are 3 options.
    
        1) Physical, these are skills that rely more on you physically doing something.
        2) Mental, these are skills that rely more on you thinking about something.
        3) Social, these are skills that rely more on you interacting with other.
        
        Please select 1: Physical, 2: Mental, 3: Social
        """)
    pillar_choice = input(f"Which pillar does '{clean_skills}' belong to? 1, 2, or 3: ")
    target_pillar = pillar_map.get(pillar_choice)
    return target_pool, clean_skills, target_pillar

def vocation_menu(voc_type): #allows player to select a job, then returns the name and age of job
    #Explain the SOC menu selection
    print("Using the US Dept of Labor SOC list, we will drill down your job by categories.\n")
    # establish what level we are on (major, minor, broad, detailed, name)
    category_names = ["Major Group", "Minor Group", "Broad Group", "Detailed Occupation", "Name"]
    current_step = 0
    prefixes = ["","","",""]
    choice = 0
    job_age = None
    while current_step <= 3:
        # use the current step to create a variable to get the right list
        search_prefix = "" if current_step == 0 else prefixes[current_step - 1]
        # build list
        job_category_list = get_data_by_level(data.SOC_FILENAME, category_names[current_step], search_prefix)
        print(f"Which {category_names[current_step]} would job your new job fall under?\n")
        if current_step > 0: print("Enter 0 to go back\n")
        for i, group in enumerate(job_category_list, 1): #print the selections for the level we are at
            print(f"{i}. {group['name']}")  # print the list
        try:
            choice = int(input("\nEnter the number of your choice (0 to go back a step): ")) #ask for selection
            if choice == 0 and current_step >= 1: #record the selection and go to next step or go back
                prefixes[current_step - 1] = ""
                current_step -= 1
                continue # Send back the lower step
            choice -= 1
        except ValueError:
            print("Please enter a valid number (or 0 to go back).")
        if 0 <= choice < len(job_category_list):
            selected = job_category_list[choice]
            if current_step == 0: prefixes[current_step] = selected['code'][:2]
            elif current_step == 1: prefixes[current_step] = selected['code'][:5]
            elif current_step == 2: prefixes[current_step] = selected['code'][:6]

            if current_step == 3:
                confirm = input(f"Confirm {selected['name']} to be correct? (y/n): ")
                if confirm.lower() == "y":
                    job_name = selected['name']
                    print(f"\nYou selected: {job_name} (Group {prefixes[current_step-1]})")
                    if voc_type == "active":
                        job_age = int(input(f"How many years have you done {job_name}? Enter a number: "))
                    elif voc_type == "retired":
                        job_age = int(input(f"How many years has it been since you were a {job_name}? Enter a number: "))
                    return job_name, job_age

                else: #send it back a step if they do not specifically type y or Y
                    current_step -= 1
                    continue  # Send back the lower step
            current_step += 1


if __name__ == "__main__": #for testing
    test_player_vocations=[]
    test_voc_type = input("active or retired: ")
    test_voc_skills = []
    test_player_vocations = vocation_questions(test_player_vocations, test_voc_type, test_voc_skills)
    print (test_player_vocations)