f = open("Day4PuzzleInput.txt")
l = []
passport = dict()
valid = 0
for item in f:
    if item == "\n":
        l.append(passport)
        passport = dict()
        continue
    values = item.split(" ")
    for i in values:
        pair = i.split(":")
        #print(pair)
        passport[pair[0]] = pair[1]
        
for j in l:
    print(j.keys())
    if 'ecl' not in j:
        continue
    if 'pid' not in j:
        continue
    if 'eyr' not in j:
        continue
    if 'hcl' not in j:
        continue
    if 'byr' not in j:
        continue
    if 'iyr' not in j:
        continue
    if 'hgt' not in j:
        continue
    valid += 1

print(valid)       
print(l)