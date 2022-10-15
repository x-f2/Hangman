import sys
import random

if __name__ == "__main__":
	if len(sys.argv) - 1 < 1:
		print("Not enough arguments.")
		exit(1)
	filename = sys.argv[1]
	with open(filename) as f:
		lines = f.readlines()
		index = random.randrange(len(lines))
		phrase = lines[index]
		print(phrase, end="")