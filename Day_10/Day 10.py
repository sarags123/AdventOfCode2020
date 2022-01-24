with open("Day10PuzzleInput.txt", "r") as fp:
    lines = [int(line.rstrip()) for line in fp.readlines()]
#opening the file and reading it line by line
one_jolt = 0
two_jolt = 0
three_jolt = 0 
outlet_rating = 0
lines.append(max(lines)+3) # because max jolt is added
#setting variables

while True: #making a while loop to go through the lines and find rating
    #adding one to each variable depending on outlet rating 
    if (outlet_rating + 1) in lines:
        one_jolt+=1
        outlet_rating += 1
    elif outlet_rating+2 in lines:
        two_jolt+=1
    elif (outlet_rating + 3) in lines:
        three_jolt += 1
        outlet_rating+=3
    else:
        break
print(one_jolt*three_jolt)