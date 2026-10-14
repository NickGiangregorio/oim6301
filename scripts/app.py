import bmi

#result = bmi.compute_bmi(80, 1.82)
#print(f"Your BMI is {result:.2f}.")



people = [
    {"name": "Alex", "height": 1.75, "weight": 70},
    {"name": "Jordan", "height": 1.68, "weight": 65},
    {"name": "Taylor", "height": 1.82, "weight": 78},
    {"name": "Morgan", "height": 1.60, "weight": 58},
    {"name": "Casey", "height": 1.73, "weight": 72},
    {"name": "Riley", "height": 1.90, "weight": 86},
    {"name": "Jamie", "height": 1.66, "weight": 62},
    {"name": "Avery", "height": 1.78, "weight": 74},
    {"name": "Cameron", "height": 1.71, "weight": 68},
    {"name": "Quinn", "height": 1.85, "weight": 82},
    {"name": "Drew", "height": 1.63, "weight": 60},
    {"name": "Reese", "height": 1.76, "weight": 75},
    {"name": "Skyler", "height": 1.69, "weight": 64},
    {"name": "Parker", "height": 1.88, "weight": 90},
    {"name": "Rowan", "height": 1.72, "weight": 71},
    {"name": "Emerson", "height": 1.58, "weight": 54},
    {"name": "Finley", "height": 1.80, "weight": 79},
    {"name": "Dakota", "height": 1.67, "weight": 66},
    {"name": "Harper", "height": 1.74, "weight": 69},
    {"name": "Logan", "height": 1.92, "weight": 94},
]

for person in people:
    print(person)
    weight = person["weight"]
    height = person["height"]   
    bmi_value = bmi.compute_bmi(weight, height)
    category = bmi.classify_bmi(bmi_value)
    print(f"{person['name']}'s BMI is {bmi_value:.2f}, and their category is {category}.")