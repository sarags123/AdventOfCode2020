l = []
valid = 0
valid2 = 0
f = open("Day2PuzzleInput.txt")
for item in f.readlines():
    l = item.split(" ")
    minmax = l[0].split("-", maxsplit=1)
    min = int(minmax[0])
    max = int(minmax[1])
    lettersplit = l[1].split(":")
    letter = lettersplit[0]
    password = l[2]
    if(password != ""):
        count = 0
        for i in password:
            if(i == letter):
                count = count + 1
        if(count >= min):
           if(count <= max):
                valid = valid + 1
    if((password[min-1] == letter) or (password[max-1] == letter)):
        valid2 = valid2 + 1
        if((password[min-1] == letter) and (password[max-1] == letter)):
            valid2 = valid2 - 1
print(valid)
print(valid2)


            
    
    
    