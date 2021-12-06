f = open("Day5PuzzleInput.txt")
rowlowerIndex = 0
rowupperIndex = 127
row = 0
col = 0
collowerIndex = 0
colupperIndex = 7
idList = []
ID = 0
for item in f.readlines():
    rowlowerIndex = 0
    rowupperIndex = 127
    row = 0
    col = 0
    collowerIndex = 0
    colupperIndex = 7
    for i in item:
        if i == 'F': #f takes the lower half
            rowupperIndex = int((rowlowerIndex+rowupperIndex+1)/2) - 1
        elif i == 'B': #b takes the upper half
            rowlowerIndex = int((rowlowerIndex+rowupperIndex+1)/2)
        elif i == 'L': #l takes the lower half
            colupperIndex = int((collowerIndex+colupperIndex+1)/2) - 1
        elif i == 'R': #r takes the upper half
            collowerIndex = int((collowerIndex+colupperIndex+1)/2)

    row = rowlowerIndex
    col = collowerIndex
    ID = row * 8 + col
    idList.append(ID)
bigID = 0
for passID in idList: 
    if passID > bigID :
        bigID = passID
print(bigID)
print(idList)

    