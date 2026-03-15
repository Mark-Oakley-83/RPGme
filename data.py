#TODO find more universal constants
from datetime import datetime

TOTAL_PLAYER_INTERVIEW_HITS = 40
SOC_FILENAME = 'soc_structure_2018.csv'
VOC_SKILLS_FILENAME = 'rpg_vocation_master_final.csv'
UNIVERSAL_SKILLS = [{
            "Instinct Pool": {"Alertness", "Social Cues", "Intuition"},
            "Training Pool": {"Coordination", "Technique", "Maintenance"},
            "Scholarship Pool": {"Research", "Analysis", "Instruction"}
            }]
UNIVERSAL_ATTRIBUTES = [{
            "Physical Pillar": {"Strength", "Fortitude", "Dexterity"},
            "Mental Pillar": {"Wisdom", "Perception", "Ingenuity"},
            "Social Pillar": {"Empathy", "Composure", "Conviction"},
            "Worldly Pillar": {"Aura"}
            }]
VOCATION_SKILLS_FILENAME = 'rpg_vocation_master_final.csv'
CURRENT_YEAR = datetime.now().year