f = open("Day7PuzzleInput.txt") 

rules = {}
for rule in f:
    rule = rule.split(" bags contain ")
    rule[1] = rule[1].split(",")
    bags = []
    for bag in rule[1]:
        bag = bag.strip(" ")
        bags.append(bag.split(" "))
    contained_bags = []
    for bag in bags:
        bag = bag[1] + " " + bag[2]
        contained_bags.append(bag)
    if "other" in contained_bags[0]:
        contained_bags[0] = "None"
    rules[rule[0]] = contained_bags

bags = ["shiny gold"]

for bag in bags:
    for rule in rules:
        if bag in rules[rule]:
            if rule not in bags:
                bags.append(rule)

print(len(bags) - 1)