import csv
import data
from char_gen_models import add_vocation


def get_data_by_level(filename, level_column, prefix):
    items = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row[level_column]
            # Check if this row is the level we want and matches our prefix
            if code and code.startswith(prefix):
                items.append({'code': code, 'name': row['Name']})
    return items


def vocation_questions():
    print("""
    Let's set up your jobs and descriptions...
    This will determine your starting skills and other features.
    Since there are so many job descriptions available, we will use the government's choices.
    Because we all know the government is paid to be efficient and accurate.
    (If you have a very very unusual job, we can deal with that in another step, for now....
     """)
    while True:
        try:
            num_of_jobs = input("\nHow many jobs do you have? please enter 1,2,or 3: ")
            num_of_jobs = int(num_of_jobs)
            if num_of_jobs > 3:
                print("Please enter up to 3; if you have more than 3, please choose 3 and we will work with it.")
                # The loop continues because we haven't 'broken' out yet
            elif num_of_jobs < 1:
                print("Please enter a number between 1 and 3.")
            else:
                # Valid input received! Break the loop to continue the rest of the program
                break
        except ValueError:
            print("Please enter 1,2 or 3: ")
    major_prefix = 00
    minor_prefix = ""
    broad_prefix = ""
    while int("num_of_jobs") >= 1:
        # 1. Load the data
        major_list = get_data_by_level(data.SOC_FILENAME, "Major Group", "")
        # 2. Display the prompt and the list
        print("Which Major Category would your job fall under?\n")
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
        print("Which Minor Category would your job fall under?\n")
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
        print("Which Broad Category would your job fall under?\n")
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

        job_list = get_data_by_level(data.SOC_FILENAME, "name", broad_prefix)
        # 2. Display the prompt and the list
        print("Which best describes your job?\n")
        for i, group in enumerate(job_list, 1):
            print(f"{i}. {group['name']}")
        # 3. Get User Input
        job_number = ""
        try:
            choice_idx = int(input("\nEnter the number of your choice: ")) - 1
            if 0 <= choice_idx < len(job_list):
                selected_job = job_list[choice_idx]
                print(f"\nYou selected: {selected_job['name']} ")
                job_number = selected_job["Detailed Occupation"]
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

        add_vocation(job_number)

        num_of_jobs -= 1
