Python Assignment (#5 Psychopy: Matching pennies)
Submission: 07.08.2020
Author: Elisabeth Kind

How to use the program:
* set working directory by typing the following into the console (replace dir_path with path to your desired 
  working directory - e.g. c:\\Users\\uname\\desktop\\python):
	import os
	os.chdir("dir_path")
* make sure all of the following files are stored in this directory:
	- 'Assignment_Functions.py'
	- 'Assignment - Matching pennies.py' 
	- 'test.csv' (needed for testing in the Assignment_Functions file)
	- 'trials.csv' (specifying the number of trials)
	- all four images ('heads-heads.jpg', 'heads-tails.jpg', 'tails-heads.jpg', 'tails-tails.jpg')
* open the 'Kind_Assignment_Functions.py' file
* run this program to make sure all functions are running properly (see output from test section)
* open the 'Kind_Assignment.py' file in Python
* run the program and follow all instructions in the console and then on the screen

INPUTS (in console):
* subject id (the subject's response data will be stored in a file with the same name):
  specify a subject id using only letters and/or numbers - e.g. '10'
* strategy (computer always switching its choice from its choice on the previous round): type 'yes' or 'no'
* p_heads: specify a probability value of heads (vs. tails) between 0 and 1 - e.g. '0.6' for 60% chance of 
  heads and 40% chance of tails

OUTPUT:
* csv file containing all responses, named after the subject id - e.g. '10.csv'
	-> if file name already taken, a new file name will be generated automatically - e.g. '10_2.csv'

HOW TO MAKE SOME CHANGES:
* to change the keys used to make a response:
	- open 'Kind_Assignment.py'
	- specify keys via the dictionary keys corresponding to 'heads-up', 'tails-up', and 'quit' (line 99)
	- save before running the program again
* to change the number of trials:
	- open the 'trials.csv' file
	- extend the TrialNumber column (each new row adds a new trial)
	- save it