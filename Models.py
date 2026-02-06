#AI Generated code to be verified
# models.py
class CharacterSheet:
    def __init__(self, name, birthday):
        self.profile = {
            "name": name,
            "birthday": birthday,
            "active_vocation": [],
            "hobbies": []
        }
        self.attributes = {
            "Physical Pillar": {"Strength": 0, "Fortitude": 0, "Dexterity": 0},
            "Mental Pillar": {"Wisdom": 0, "Perception": 0, "Ingenuity": 0},
            "Social Pillar": {"Emotional Intelligence": 0, "Composure": 0, "Conviction": 0},
            "Worldly Pillar": {"Aura": 0}
        }

    def add_vocation(self, new_vocation):
        """Adds a vocation only if the character has fewer than 3."""
        if len(self.profile["active_vocations"]) < 3:
            self.profile["active_vocations"].append(new_vocation)
        else:
            print("Maximum active vocations (3) reached.")