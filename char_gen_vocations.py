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


def vocation_questions(player_vocations, voc_type):
    #get the voc_type and present the player with 2 greetings
    num_jobs = 0
    if voc_type == "active":
        print(f"""
            Let's set up your jobs and descriptions...
            We are setting the limit for active vocations to 3, if you have more than that
            we can add them as hobbies later.
            This will determine your starting skills and other features.
            Since there are so many job descriptions available, we will use the government's choices.
            Because we all know the government is paid to be efficient and accurate.
            (If you have a very very unusual job, we can deal with that in another step, for now....
            """)
        num_jobs = int(input("\nHow many jobs do you have? Enter 1,2, or 3: "))
    elif voc_type == "retired":
            print(f"""
                Let's set up your old jobs and descriptions...
                These will give you credit for jobs you have done in the past.
                Since there are so many job descriptions available, we will use the government's choices.
                Because we all know the government is paid to be efficient and accurate.
                (If you have a very very unusual job, we can deal with that in another step, for now....
                """)
            num_jobs = int(input("\nHow many jobs do you have? Enter a number: "))
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
        #append the player sheet
        player_vocations.append({'name': job_name, 'age': job_age})
        #reduce the num of jobs
        num_jobs -= 1
    else:
        print(f"These are now your {voc_type} vocations!\n")
        print(player_vocations)

    return player_vocations

def vocation_menu(voc_type):
    #Explain the SOC menu selection
    print("Using the US Dept of Labor SOC list, we will drill down your job by categories.")
    # establish what level we are on (major, minor, broad, detailed, name)
    category_names = ["Major Group", "Minor Group", "Broad Group", "Detailed Occupation", "Name"]
    current_step = 0
    prefixes = ["","","",""]
    choice = 0
    job_age = None
    while current_step <= 4:
        # use the current step to create a variable to get the right list
        search_prefix = "" if current_step == 0 else prefixes[current_step - 1]
        # build list
        job_category_list = get_data_by_level(data.SOC_FILENAME, category_names[current_step], search_prefix)
        print(f"Which {category_names[current_step]} would job your new job fall under?\n")
        if current_step > 0: print("Enter 0 to go back\n")
        for i, group in enumerate(job_category_list, 1): #print the selections for the level we are at
            print(f"{i}. {group['name']}")  # print the list
        try:
            choice = int(input("\nEnter the number of your choice: ")) #ask for selection
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
            elif current_step == 3: prefixes[current_step] = selected['code']

            if current_step == 4:
                confirm = input(f"Confirm {selected['name']} to be correct? (y/n): ")
                if confirm.lower() == "y":
                    job_name = selected['name']
                    print(f"\nYou selected: {selected} (Group {prefixes[current_step-1]})")
                    if voc_type == "active":
                        job_age = int(input(f"How many years have you done {selected}? Enter a number: "))
                    elif voc_type == "retired":
                        job_age = int(input(f"How many years has it been since you were a {selected}? Enter a number: "))
                    return job_name, job_age

                else: #send it back a step if they do not specifically type y or Y
                    current_step -= 1
                    continue  # Send back the lower step
            current_step += 1



if __name__ == "__main__":
    test_player_vocations=[]
    test_voc_type = input("active or retired: ")
    test_player_vocations = vocation_questions(test_player_vocations, test_voc_type)
    print (test_player_vocations)