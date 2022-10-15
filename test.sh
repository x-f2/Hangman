#/bin/bash

##
# Tests Hangman.py Application
# If no arguments are given, defaults to a random sentence
#   in the file ./random-sentences.txt
# Else, uses the evaluated result of proceeding string as sh command
#   e.g. "./test.sh echo This is my phrase" or "./test.sh fortune"
##


filename="random-sentences.txt"
phrase="$(python ./RandomSentence.py $filename)"

if [[ $# -ge 1 ]]; then
	phrase="$(eval $@)"
fi

python ./Hangman.py "$phrase"
