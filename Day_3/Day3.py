f = open("Day3PuzzleInput.txt")
l = [] #creates empty list to add variables to after split
valid = 0 #initializes variable to determine the number of valid passwords in Day 2 part 1
valid2 = 0 #initializes variable to determine the number of valid passwords in Day 2 part 2
f = open("Day2PuzzleInput.txt") #opens text file with passwords and requirements
for item in f.readlines(): #loops through each line in text file
    l = item.split(" ") #splits each line in text file by a spaces creating a list with three parts 
    minmax = l[0].split("-", maxsplit=1) #splits the first part of the list into another list seperated by the - to find min and max
    min = int(minmax[0])#makes the min an integer and takes the first index of minmax
    max = int(minmax[1])#makes the max an integer and takes the second index of minmax
    lettersplit = l[1].split(":") #splits the colon away from the letter
    letter = lettersplit[0] #makes the letter equal to the first index of the list with the letter and colon
    password = l[2] #sets the password equal to the third index in list l
    if(password != ""): #checks to make sure password exists
        count = 0 #resets count for each password
        for i in password: #loops through each letter in password
            if(i == letter): #checks if letter if equal to given letter
                count = count + 1 #when letter is equal to given letter adds one to the count to determine how many times the letter occurs in the password
        if((count >= min) and (count <= max)):#checks to make sure the count is greater than min amount and less than max amount of times letter can occur for password to be valid
                valid = valid + 1 #adds one to valid if count fits requirements
    #part 2
    if((password[min-1] == letter) or (password[max-1] == letter)): #checks if either of the positions stated in text file contain the letter
        valid2 = valid2 + 1 #if either position has the letter then add one to valid so number of valid passwords increase
        if((password[min-1] == letter) and (password[max-1] == letter)): #checks to see if the password has the letter in both positions
            valid2 = valid2 - 1 #if letter is in both positions then subtract one from the number of valid passwords because it is only valid if letter is in only one of the positions
print(valid) #prints out the number of valid passwords for part 1
print(valid2) #prints out the number of valid passwords for part 2


            
    
    
    
