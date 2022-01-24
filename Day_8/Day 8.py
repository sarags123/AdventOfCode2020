with open("Day 8 Puzzle Input.txt", "r") as fp:
    lines = fp.readlines()
    lines = [line.rstrip() for line in lines]
# reading the file line by line

# creating a function to do challenge 1
def challenge1(lines):
    curr_acc = 0
    visited_line = set()
    curr_line = 0

    while True: 

        inst, acc = lines[curr_line].split(" ") #splits instruction and number
        acc = int(acc)
        visited_line.add(curr_line)

        if inst == "nop":
            curr_line += 1 #next line if nop
        if inst == "acc":
            curr_acc += acc
            curr_line += 1  #increase the accumulator and go to next line
        if inst == "jmp":
            curr_line+=acc #go to the below or above current line depending on number next to jump

        if valid_sol == False:
            return curr_acc, True 
    return curr_acc, False
print("Current Accumulator: ", challenge1(lines)[0]) #prints answer