f = open("Day6PuzzleInput.txt")
answers = []
answer = []

for i in f.readlines(): #looping through file
    if i != '\n': #exludes empty lines
        for question in i[:-1]: #makes sure not to include the new line
            if question not in answer:
                answer.append(question) #taking out repeat letters
    else:
        answers.append(len(answer))
        answer = []
answers.append(len(answer)) #doing last group

print(sum(answers))#finding sum

