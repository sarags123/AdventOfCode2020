# f = open("Day3PuzzleInput.txt")
# trees = '#'
# space = '.'
# count = 0
# tcount = 0
# l = []
#  
# while 1:
#      
#     # read by character
#     char = f.read(1)         
#     if not char:
#         break
#     l.append(char)
# print(l)
# for i in l:
#     if(l[count] == trees):
#         tcount = tcount + 1
#     count = count + 34
inputfile = open('Day3PuzzleInput.txt', 'r') #opening puzzle input in read mode

# Parse lines
data = [x.strip() for x in inputfile.readlines()] #going through each line and making it set to data variable
def part1(data):
    x = 0                             # X is current column
    total = 0                         # Count of trees
    map_width = len(data[0])          #defines the number of columns
    map_height = len(data)            #defines the number of rows
    for y in range(map_height):       # Iterate each row
        if data[y][x] == '#':         # Use x,y as coordinates to check for tree
            total += 1                # Count if tree
        x = (x + 3) % map_width       # Jump 3 steps right 
    return total

print ("Solution part 1: %d" % part1(data)) #print part 1 solution
def part2(data):                            #part 2 method
    def traverse(right, down):              # Define a function for generalizing
        x = 0  
        total = 0
        for i in range(len(data)):
            if i % down != 0:               # Skip rows according to "down"-variable
                continue
            if data[i][x] == '#':
                total += 1
            x = (x + right) % len(data[0])  # Use right-parameter
        return total

    # Use function to get values for each slope
    return traverse(1,1) * traverse(3,1) * traverse(5,1) * traverse(7,1) * traverse(1,2) #defining different slopes
print ("Solution part 2: %d" % part2(data)) #prints part 2 solution