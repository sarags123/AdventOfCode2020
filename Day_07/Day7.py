f = open("Day7PuzzleInput.txt") 

rules = {} #creating a list of rules with shiny gold bag
for rule in f:
    rule = rule.split(" bags contain ") #split between bag and what is inside bag
    rule[1] = rule[1].split(",") #splits between different bags inside of bag
    bags = [] #creating a list of bags
    for bag in rule[1]: #looping through different bags inside of bag
        bag = bag.strip(" ")
        bags.append(bag.split(" "))#removes the number
    contained_bags = []
    for bag in bags: 
        bag = bag[1] + " " + bag[2]
        contained_bags.append(bag)
    if "other" in contained_bags[0]:
        contained_bags[0] = "None"
    rules[rule[0]] = contained_bags

bags = ["shiny gold"]

for bag in bags: #for loop to append the bag to the bags list if it has shiny gold 
    for rule in rules:
        if bag in rules[rule]:
            if rule not in bags:
                bags.append(rule)

print(len(bags) - 1)