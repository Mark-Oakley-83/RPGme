import math

import pandas as pd
from data import CURRENT_YEAR

def skill_weight_calc(player_sheet):
    #define variables I am pretty sure I will need
    char_v_skills = player_sheet.voc_skills #pull custom skills
    char_u_skills = player_sheet.universal_skills
    char_h_skills = player_sheet.hobby_skills
    char_foundation = player_sheet.profile['foundation']
    char_zodiac = player_sheet.profile["zodiac"]

    # Combines all three dictionaries into one flat zeroed-out map
    master_pools = [char_u_skills,  char_v_skills, char_h_skills]
    all_skills_list = { #This will create a list of all skills with a value of 0
        skill: 0
        for source in master_pools
        for pool in source.values()
        for skill in pool.keys()
    }
    # apply Foundation skill weights (this might be done better to avoid hard coding, but maybe not
    if char_foundation == "Academic":
        all_skills_list["Research"] += 4
        all_skills_list["Analysis"] += 4
        all_skills_list["Instruction"] += 4
    if char_foundation == "Trade":
        all_skills_list["Coordination"] += 4
        all_skills_list["Technique"] += 4
        all_skills_list["Maintenance"] += 4
    if char_foundation == "Street":
        all_skills_list["Alertness"] += 4
        all_skills_list["Social Cues"] += 4
        all_skills_list["Intuition"] += 4
    if char_foundation == "Military":
        all_skills_list["Coordination"] += 2
        all_skills_list["Technique"] += 2
        all_skills_list["Maintenance"] += 2
        all_skills_list["Alertness"] += 1
        all_skills_list["Social Cues"] += 1
        all_skills_list["Intuition"] += 1
        all_skills_list["Research"] += 1
        all_skills_list["Analysis"] += 1
        all_skills_list["Instruction"] += 1
#apply vocation skill weights
    #read the vocations skills list
    data_vocation = pd.read_csv('rpg_vocation_master_final.csv')
    #create a local dictionary of jobs and associated skills
    vocation_map = {
        #find the "unique job name" from the list and pull the 3 skills from the skills column
        row['Unique job name']: [s.strip() for s in row['Universal Skills'].split(',')]
        for _, row in data_vocation.iterrows()
    }
#pull the vocations and their age
    char_a_voc_list = player_sheet.profile["active_vocations"]
    char_r_voc_list = player_sheet.profile["retired_vocations"]
    active_skills_in_use = set()
    for job in char_a_voc_list: #crate a list of active skills
        active_skills_in_use.update(vocation_map.get(job['name'], []))
    vocation_skill_adjust(char_a_voc_list, vocation_map, all_skills_list, 'active', active_skills_in_use) #adjust active
    vocation_skill_adjust(char_r_voc_list, vocation_map, all_skills_list, 'retired', active_skills_in_use) #adjust retired
#add weights to special vocation skills
    for skills_list in char_v_skills.values():
        for skill, skill_data in skills_list.values():
            is_active = (skill_data.get('length', 0) == 0) #dirty flag for active vocation skills sets is_active to true if the skill is currently active in vocations
            tenure = int(skill_data['age'])
            adjust = 0
            if tenure <= 5: adjust = 1
            elif 6 <= tenure <= 10: adjust = 3
            elif 11 <= tenure <= 15: adjust = 5
            elif 16 <= tenure <= 25: adjust = 7
            elif tenure >= 26: adjust = 10
            if is_active: #skills from active vocations
                all_skills_list[skill] += adjust
            else: #skills from retired vocations
                all_skills_list[skill] -= max(0, all_skills_list.get(skill, 0) - adjust)
    for pool_name, pool_dict in char_h_skills.items():
        for skill, skill_data in pool_dict.items():
            is_active = (int(skill_data['last_used']) == CURRENT_YEAR)
            tenure = int(skill_data['Years_Active'])
            years_since_active = (int(skill_data['last_used'] - CURRENT_YEAR))
            adjust = 0
            if tenure <= 5: adjust = 1
            elif 6 <= tenure <= 10: adjust = 3
            elif 11 <= tenure: adjust = 5 #hobbies are maxed at Journeyman level so any additional years would be moot
            if not is_active:
                if years_since_active <= 1: adjust -= 1
                elif 6 <= years_since_active <= 10: adjust -= 3
                elif 11 <= years_since_active: adjust -= 5
            all_skills_list[skill] += adjust
#Add in Moon sign bonuses
    pool_mapping = {
        "Instinct": ["Alertness", "Social Cues", "Intuition"],
        "Training": ["Coordination", "Technique", "Maintenance"],
        "Scholarship": ["Research", "Analysis", "Instruction"]
    }
    char_moon = player_sheet.profile["moon_sign"]
    moon_data = pd.read_csv('moon_phases.csv')
    phase_data = moon_data.loc[moon_data['Phase'] == char_moon]
    if len(phase_data) > 0:#if the value is not empty
        row_dict = phase_data.to_dict('records')[0]
        targets = [row_dict['first'], row_dict['second']]
        for pool in targets:
            if pool in pool_mapping:
                for skill in pool_mapping[pool]:
                    all_skills_list[skill] += 2
# Zodiac adjustments:
    #Load the Zodiac CSV
    zodiac_df = pd.read_csv('zodiac_bonuses.csv')
    #Find the row for the player's sign
    zodiac_row = zodiac_df[zodiac_df['Sun Sign'] == char_zodiac]
    if not zodiac_row.empty:
        # Pull the "Unique" pool target
        target_pool = zodiac_row.iloc[0]['Unique']
        # Apply the +1 nudge to all skills in that pool
        if target_pool in pool_mapping:
            for skill in pool_mapping[target_pool]:
                all_skills_list[skill] += 1
#weight converted to points
    skill_hits = sum(all_skills_list.values())
    skill_final_percentages = {}
    if skill_hits > 0:
        for skill, hits in all_skills_list.items():
            # Calculate the weight as a decimal (e.g., 0.1534)
            percentage = hits / skill_hits
            # Rounding to 4 decimal places gives you clean percentages (e.g., 15.34%)
            skill_final_percentages[skill] = round(percentage, 4)
    else:
        # Safety fallback for a brand new character with no history
        for skill in all_skills_list:
            skill_final_percentages[skill] = 0.1111
    char_skill_points = (player_sheet.profile["age"] - 15) * 3
    assigned_points = {}
    remainders = {}
    total_assigned = 0
    for skill, weight in skill_final_percentages.items():
        exact_value = weight * char_skill_points
        assigned_points[skill] = math.floor(exact_value)
        remainders[skill] = exact_value - assigned_points[skill]
        total_assigned += assigned_points[skill]
    #set the leftovers for remainder assignment
    leftover = char_skill_points - total_assigned
    #sort the remainders highest to lowest
    sorted_by_remainder = sorted(remainders.items(), key=lambda x: x[1], reverse=True)
    #run this for each point left over until all points are used
    for i in range(leftover):
        attr_to_boost = sorted_by_remainder[i][0]
        assigned_points[attr_to_boost] += 1
    for update_skill, tally in assigned_points.items():
        categories = ["universal_skills", "voc_skills", "hobby_skills"]
        for cat in categories:
            for pool in player_sheet.profile[cat]:
                skill_box = player_sheet.profile[cat][pool]
                # Check if the skill belongs in this specific pool
                if update_skill in skill_box:
                    if tally >= 11:
                        skill_box[update_skill] = tally - 10
                        player_sheet.skill_master.append(update_skill)
                    else:
                        skill_box[update_skill] = tally
                    break


def vocation_skill_adjust(voc_list, voc_map, all_char_skills, voc_type, active_skills):
    for entry in voc_list:  # for each job in the list
        job_name = entry['name']  # pull the name
        if voc_type == 'active':
            tenure = int(entry['age'])
            length_since = 0  # pull the tenure of the job
        else:
            tenure = int(entry['tenure'])
            length_since = int(entry['age'])
        if job_name in voc_map:  # double checks that the job is correct
            for skill in voc_map[job_name]:  # for each skill associated for the job (active and retired)
                adjustment = 0
                if tenure <= 5:  # adjust the weight of the skill based on the length of time in the job
                    adjustment += 1
                elif 6 <= tenure <= 10:
                    adjustment += 3
                elif 11 <= tenure <= 15:
                    adjustment += 5
                elif 16 <= tenure <= 25:
                    adjustment += 7
                elif tenure >= 26:
                    adjustment += 10
                if voc_type == 'retired' and skill not in active_skills:
                    if all_char_skills[skill] > 0:
                        if length_since <= 5:
                            adjustment -= 1
                        elif 5 <= length_since <= 10:
                            adjustment -= 3
                        elif 10 <= length_since <= 15:
                            adjustment -= 5
                        elif 15 <= length_since <= 25:
                            adjustment -= 7
                        elif int(length_since) >= 26:
                            adjustment -= 10
                all_char_skills[skill] = max(0, all_char_skills[skill] + adjustment)




    #send the calculations back to char_u, h, v_skills
    #return the u,h,v skills with new values

if __name__ == "__main__": #for testing
    from char_gen_models import CreateCharacterSheet
    test_player_sheet = CreateCharacterSheet("test", "1983-5-14", 42)
    skill_weight_calc(test_player_sheet)