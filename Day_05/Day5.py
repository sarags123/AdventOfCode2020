f = open("Day5PuzzleInput.txt")
rowlowerIndex = 0
rowupperIndex = 127
row = 0
col = 0
collowerIndex = 0
colupperIndex = 7
idList = []
ID = 0 #setting up possible variables to use
for item in f.readlines(): #iterating through each line of file
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
    ID = row * 8 + col #returning the id number
    idList.append(ID)
        
bigID = 0
for passID in idList: #iterating through list of ids to find the largest id
    if passID > bigID :
        bigID = passID
print(bigID)
idList.sort() #putting list of ids in ascending order
print(idList)
myID = []
for passID in idList: #finding missing boarding pass id in the list
    if (passID + 1 in idList) and (passID - 1 in idList):
        continue
    else:
        myID.append(passID)
print(myID) #will give the two id numbers of the boarding passes right next to your take the number in between for answer to pt2 
        

