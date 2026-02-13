import csv

def run_dumb_test():
    #set all attribute hits to 0
    tally = {attr: 0 for attr in ["Strength", "Dexterity", "Fortitude", "Wisdom",
                                  "Perception", "Ingenuity", "Empathy",
                                  "Composure", "Conviction", "Aura"]}

    print("--- WELCOME TO THE D.U.M.B. TEST ---")
    print("(Definitive Universal Metric Battery)")
    print("Please answer all questions honestly for accurate profiling.)/n(We will be watching (-)>(-) )")
    # The "Template" for how questions look on screen
    display_template = """
------------------------------------------------------------
Question {id}: {text}

A) {A_text}
B) {B_text}
C) {C_text}
D) {D_text}
------------------------------------------------------------
"""

    with open('questions.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # 1. Ask the question using the template
            print(display_template.format(**row))

            # 2. Record the answer
            while True:
                choice = input("Select A, B, C, or D: ").upper()
                if choice in ['A', 'B', 'C', 'D']:
                    # 3. Add hits to tally
                    # We split the string "Strength,Fortitude" into a list
                    attrs_to_hit = row[f'{choice}_attrs'].split(',')
                    for attr in attrs_to_hit:
                        tally[attr.strip()] += 1
                    break
                print("Invalid choice.")

    return tally

if __name__ == "__main__":
    test_tally = run_dumb_test()
    print(test_tally)