with open("Day 8 Puzzle Input.txt", "r") as fp:
    lines = fp.readlines()
    lines = [line.rstrip() for line in lines]
# reading the file line by line

# challenge 1
def challenge1(lines):
    curr_acc = 0
    visited_line = set()
    curr_line = 0
    valid_sol = True
    while True: 

        # viewed all lines and we got lucky, no loops
        if len(lines)-1 == curr_line:
            valid_sol = False

        # for challenge 1 solution
        if curr_line in visited_line:
            valid_sol = False
            return curr_acc, valid_sol


        inst, acc = lines[curr_line].split(" ")
        acc = int(acc)
        visited_line.add(curr_line)

        if inst == "nop":
            curr_line += 1
        if inst == "acc":
            curr_acc += acc
            curr_line += 1 
        if inst == "jmp":
            curr_line+=acc

        # we got lucky
        if valid_sol == False:
            return curr_acc, True 
    return curr_acc, False
print("Current Accumulator: ", challenge1(lines)[0])

# challenge 2
def challenge2(lines):
    curr_acc = 0
    visited_line = []
    curr_line = 0
    new_lines = lines.copy()
    for curr_line in range(1, len(new_lines)):   
        inst, acc = lines[curr_line].split(" ")
        acc = int(acc)

        if inst == "nop":
            inst = "jmp"
        elif inst == "jmp":
            inst = "nop"

        visited_line = []
        new_lines = lines.copy()
        new_lines[curr_line] = " ".join((inst, str(acc)))
        acc, valid = challenge1(new_lines)
        if valid:
            return acc

print("Current Accumulator: ", challenge2(lines))    