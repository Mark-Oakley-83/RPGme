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
    if voc_type == 'retired':
        print(f"""
            Let's set up your old jobs and descriptions...
            These will give you credit for jobs you have done in the past.
            Since there are so many job descriptions available, we will use the government's choices.
            Because we all know the government is paid to be efficient and accurate.
            (If you have a very very unusual job, we can deal with that in another step, for now....
             """)
    else:
        print(f"""
            Let's set up your jobs and descriptions...
            This will determine your starting skills and other features.
            Since there are so many job descriptions available, we will use the government's choices.
            Because we all know the government is paid to be efficient and accurate.
            (If you have a very very unusual job, we can deal with that in another step, for now....
             """)


    while True:
        if voc_type == 'active':
            try:
                num_of_jobs = input("\nHow many jobs do you have currently? please enter 1,2,or 3: ")
                num_of_jobs = int(num_of_jobs)
                if num_of_jobs > 3:
                    print("Since we can only list 3 jobs on the character sheet \n please use just the 3 you work the most, \nand we will list the others as hobbies for now.")
                    num_of_jobs = 3
                    break

                elif num_of_jobs < 1:
                    print("Please enter a number between 1 and 3.")
                else:
                    # Valid input received! Break the loop to continue the rest of the program
                    break
            except ValueError:
                print("Please enter 1,2 or 3: ")
        elif voc_type == 'retired':
            num_of_jobs = input("\nHow many old jobs would you like to add to the retired list?")
            num_of_jobs = int(num_of_jobs)
            break
    print("\n We will do this in layers for each job.")
    major_prefix = 00
    minor_prefix = ""
    broad_prefix = ""
    run_through = 1
    years = 0
    while num_of_jobs >= 1:
        #Load the data
        major_list = get_data_by_level(data.SOC_FILENAME, "Major Group", "")
        #Display the prompt and the list
        print(f"Which Major Category would job your #{run_through} job fall under?\n")
        for i, group in enumerate(major_list, 1):
            print(f"{i}. {group['name']}")
        # 3. Get User Input
        try:
            choice_major = int(input("\nEnter the number of your choice: ")) - 1
            if 0 <= choice_major < len(major_list):
                selected_major = major_list[choice_major]
                # We store the 2-digit prefix (e.g., '11' from '11-0000') for the next step
                major_prefix = selected_major['code'][:2]
                print(f"\nYou selected: {selected_major['name']} (Group {major_prefix})")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

        minor_list = get_data_by_level(data.SOC_FILENAME, "Minor Group", major_prefix)
        # 2. Display the prompt and the list
        print(f"Which Minor Category would your #{run_through} {voc_type} job fall under?\n")
        for i, group in enumerate(minor_list, 1):
            print(f"{i}. {group['name']}")
        # 3. Get User Input
        try:
            choice_idx = int(input("\nEnter the number of your choice: ")) - 1
            if 0 <= choice_idx < len(minor_list):
                selected_minor = minor_list[choice_idx]
                # We store the 4-digit prefix (e.g., '11-10' from '11-1000') for the next step
                minor_prefix = selected_minor['code'][:5]
                print(f"\nYou selected: {selected_minor['name']} (Group {minor_prefix})")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

        broad_list = get_data_by_level(data.SOC_FILENAME, "Broad Group", minor_prefix)
        # 2. Display the prompt and the list
        print(f"Which Broad Category would your #{run_through} {voc_type} job fall under?\n")
        for i, group in enumerate(broad_list, 1):
            print(f"{i}. {group['name']}")
        # 3. Get User Input
        try:
            choice_idx = int(input("\nEnter the number of your choice: ")) - 1
            if 0 <= choice_idx < len(broad_list):
                selected_broad = broad_list[choice_idx]
                # We store the 6-digit prefix (e.g., '11-101' from '11-1010') for the next step
                broad_prefix = selected_broad['code'][:6]
                print(f"\nYou selected: {selected_broad['name']} (Group {broad_prefix})")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

        job_list = get_data_by_level(data.SOC_FILENAME, "Detailed Occupation", broad_prefix)
        # 2. Display the prompt and the list
        print(f"Which best describes your #{run_through} {voc_type} job?\n")
        for i, group in enumerate(job_list, 1):
            print(f"{i}. {group['name']}")
        # 3. Get User Input
        job_number = ""
        try:
            choice_idx = int(input("\nEnter the number of your choice: ")) - 1
            if 0 <= choice_idx < len(job_list):
                selected_job = job_list[choice_idx]
                print(f"\nYou selected: {selected_job['name']} ")
                job_number = selected_job["name"]
                if voc_type == 'retired':
                    years = input(f"How many years were you a {selected_job["name"]}? ")
                elif voc_type == 'active':
                    years = input(f"How many years have you been a you a {selected_job["name"]}? ")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

        can_add = add_vocation(player_vocations, job_number, years)
        if not can_add and voc_type == "active":
            print("Maximum active vocations (3) reached.")
        else:
            print(f"Success! {job_number} added to your active vocations.")
        run_through += 1
        num_of_jobs -= 1

    return player_vocations

def add_vocation(vocation_list, new_vocation, years):
    """Adds a vocation only if the character has fewer than 3."""
    if len(vocation_list) <= 3:
        vocation_list.append({"name": new_vocation, "years": years})
        return True
    else:
        return False

if __name__ == "__main__":
    test_player_vocations=[]
    test_voc_type = input("active or retired: ")
    test_player_vocations = vocation_questions(test_player_vocations, test_voc_type)
    print (test_player_vocations)