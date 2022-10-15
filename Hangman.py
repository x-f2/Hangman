import sys
import os
import random

##
# Hangman Class.
#   written by x-2f
#   10/15/2022
##
class Hangman:
	structure = [
		["    U         |", "   (_)        |"],
		["              |", "    |         |", "   /|         |", "   /|\\        |"],
		["              |", "    |         |", "  / |         |", "  / | \\       |"],
		["              |", "   /          |", "   / \\        |"],
		["             /|", "  /          /|", "  /   \\      /|"]
	]
	processed = ()
	mistakes = 0
	phrase = ""
	show_title = False
	responses = {
		"correct": {
			"index": 0,
			"phrases": [
				"You got it!", "Good job!", "Bullseye!",
				"That's right!", "Awesome!"
			]
		},
		"incorrect": {
			"index": 0,
			"phrases": [
				"Nope. Bummer.", "Not this time.",
				"Nada.", "Zilch."
			]
		},
		"win": {
			"index": 0,
			"phrases": [
				"Congratulations! You won."
			]
		},
		"loss": {
			"index": 0,
			"phrases": [
				"Game over. You lost.",
				"Too bad. Try again next time.",
			]
		}
	}
	##
	# Constructor.
	##
	def __init__(self, phrase):
		self.phrase = phrase
		for key in self.responses:
			size = len(self.responses[key]["phrases"])
			random.shuffle(self.responses[key]["phrases"])
			self.responses[key]["index"] = random.randrange(size)

	##
	# Prints everything.
	##
	def print(self):
		# Prints title
		if self.show_title:
			print("   H  A  N  G  M  A  N")
		# Prints top of gallows
		print("    ___________\n    |         |\n    |         |")
		count = self.mistakes
		y = 0
		# Prints middle parts which vary depending on # of mistakes
		while y < len(self.structure):
			x = 0
			while x < len(self.structure[y]) - 1 and count > 0:
				x += 1
				count -= 1
			if y == 0:
				print(self.structure[y][x])
				y += 1
			elif y % 2 == 1:
				print(self.structure[y][x])
				print(self.structure[y + 1][x])
				y += 2
		# Prints bottom of gallows
		print("            / |\n           /__|\n")
		# Prints letter set
		for i in range(0, 26):
			c = chr(i + 97)
			if c in self.processed:
				c = "-"
			print(c + " ", end="")
			if i == 12:
				print()
		print("\n")
		# Gets console width for manual wrapping
		CONSOLE_WIDTH, CONSOLE_HEIGHT = os.get_terminal_size()
		message = ""
		x = 0
		# Builds phrase
		for c in self.phrase:
			if self.isletter(c) and c.lower() not in self.processed:
				c = "_"
			message += c + " "
			x += 2
			if x >= CONSOLE_WIDTH - 10:
				print()
				x = 0
		# Prints target phrase
		print("%s\n" % message)

	##
	# Prompts user for a guess and parses it into a
	# 	lowercase letter
	# @return None if a letter can't be found
	##
	def prompt(self):
		guess = input("Guess: ")
		for c in guess.lower():
			if self.isletter(c):
				return c

	##
	# Returns whether a character is a letter
	##
	def isletter(self, character):
		return 97 <= ord(character.lower()) <= 123

	##
	# Clears standard output. Works for unix and Windows.
	##
	def clear(self):
		os.system("clear" if os.name == "posix" else "cls")

	##
	# Prints a "random" response according to the type requested
	##
	def print_response(self, key):
		index = self.responses[key]["index"]
		phrases = self.responses[key]["phrases"]
		print(phrases[index])
		index = (index + 1) % len(phrases)
		self.responses[key]["index"] = index

	##
	# Processes a guessed character and returns a code as a response
	##
	def process(self, character):
		response = 0
		if character in self.processed:
			response = 2
		else:
			self.processed += (character,)
		win = True
		for c in self.phrase:
			if self.isletter(c) and c.lower() not in self.processed:
				win = False
				break
		if win:
			response = 4
		elif character not in self.phrase.lower():
			response = 5 if self.mistakes == 5 else 1
			self.mistakes += 1
		return response
	##
	# Begins the game. Continually asks for guesses and prints
	#   out the necessary responses. The loop breaks when the
	#   the game is finished, either by a win or a loss.
	# @return True if the game was won, False otherwise
	##
	def start(self):
		last_char = ""
		response = -1
		while True:
			self.clear()
			self.print()
			match response:
				# Correct guess
				case 0: 
					self.print_response("correct")
				# Incorrect guess
				case 1:
					self.print_response("incorrect")
				# Already guessed
				case 2:
					print("'%s' already guessed." % last_char)
				# Invalid answer
				case 3:
					print("Try again.")
				# Game has been won
				case 4:
					self.print_response("win")
					break
				# Game has been lost
				case 5:
					self.print_response("loss")
					break
				case _:
					print()
			last_char = self.prompt()
			if last_char == None:
				response = 3
				continue
			response = self.process(last_char)
		# Returns whether it's a win
		return response == 4

##
# Creates and starts a game.
#   If no argument is given, the phrase will
#   be the default, "Hello, World!"
# 	Otherwise it will be the first argument given.
##
if __name__ == "__main__":
	default_phrase = "Hello, world!"
	phrase = default_phrase
	if len(sys.argv) > 1:
		phrase = sys.argv[1]
	game = Hangman(phrase)
	game.show_title = True
	win = game.start()
	if not win:
		exit(1)
