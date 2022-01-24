f = [
  int(line.strip())
  for line
  in open('Day9PuzzleInput.txt', 'r').readlines()
] #opening the file and reading it line by line
def part1(f):
    # Iterate all f
    for i, n in enumerate(f):
        # Skip "preamble"
        if i < 25:
            continue
        # Iterate all 25 previous f
        is_valid = False
        for j in range(i-25,i):
            # Try out all combinations to sum to n
            for k in range(i-25, i):
                if j != k:
                    if f[j] + f[k] == n:
                        is_valid = True
                        break
                if is_valid:
                    break
            if is_valid:
                break
        # If is not valid, then that is the answer
        if not is_valid:
            return n
print (part1(f))