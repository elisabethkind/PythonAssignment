# -*- coding: utf-8 -*-
"""
Python Assignment (#5 Psychopy: Matching pennies)
Submission: 07.08.2020
Author: Elisabeth Kind

Python script that allows a subject to play a game of matching pennies against the computer.
* subject chooses with a key press whether to present their penny heads-up or tails-up
* computer makes its choice randomly
* when the subject has made their choice, both pennies are shown on the screen
* the subject is informed whether they won that round or not, and what the current scores are
* allow the subject to quit at any round by pressing a quit key instead of making a choice

Additional features:
    * allow the experimenter to allocate the computer a different strategy, for example, biasing its choice towards heads or tails, or towards switching from its choice on the previous round
    * produce a printout of the results at the end of the program showing:
        - how often the subject switched their choice so that it was different from their choice in the previous round
        - how often the subject switched their choice so that it was different from the computer's choice in the previous round

"""

import os
import random
import pandas
import Kind_Assignment_Functions

from psychopy import visual, core, data, event

# %% Experimenter input

# Subject id
subj_id = None
while subj_id is None:
    subj_id = input('Subject_ID: ') # input subject id
    if subj_id == '': # ask again if no input given
        print("Please specify a subject id.")
        subj_id = None
        continue
    elif 1 in [c in subj_id for c in set('!"§$%&/()=?`{[]}\´~*><|^°,')]: # ask again if subject id contains special characters
        error_message = "'{}' contains special characters. Please specify a subject id only containing letters and/or numbers."
        print(error_message.format(subj_id))
        subj_id = None
        continue
    else:
        break

# Computer strategy
strategy = None
while strategy is None:
    strategy = input('Strategy (yes/no): ') # set strategy: 'yes' for switch of computer from its choice on the previous round, 'no' for no such strategy
    if strategy == '': # ask again if no input given
        print("Please specify whether a strategy shall be applied by the computer.")
        strategy = None
        continue
    elif strategy not in ['yes', 'no']:
        print("Please specify by entering either 'yes' or 'no' whether a strategy shall be applied by the computer.")
        strategy = None
        continue
    else:
        break

# Chance of heads vs. tails
p_heads = None
while p_heads is None:
    p_heads = input('P(heads): ') # set probability of heads (vs. tails) btw. 0 and 1
                                  # if strategy == 'yes', this will only affect the first choice
    if p_heads == '': # if no input, ask again
        print("Please specify the probability of heads (vs. tails) with a number between 0 and 1. Enter '0.5' for equal chances.")
        p_heads = None
        continue
    elif float(p_heads) > 1 or float(p_heads) < 0: # if input nr outside of range, ask again
        error_message = "'{}' lies outside of the range. Please specify a number between 0 and 1."
        print(error_message.format(p_heads))
        p_heads = None
        continue
    elif 1 not in [c in p_heads for c in set('0123456789.')]: # if input is not a nr, ask again
        print("Please specify a number between 0 and 1 (e.g. 0.5).")
        p_heads = None
        continue
    else:
        break

p_heads = float(p_heads)
p_tails = 1-p_heads

# %% Set up trials

# Load trials from csv file.
trial_list = data.importConditions('trials.csv') # creates list of trails
t_nr = len(trial_list) # number of trials

# Run trials 1 time in sequential order.
trials = data.TrialHandler(trial_list, 1, method='sequential')

# %% Window

win = visual.Window(color='white', fullscr=True)

# %% Keyboard

# Dictionary mapping key names (pressed on keyboard) to their meanings:
key_meanings = {'1': 'heads-up', '0': 'tails-up', 'q': 'quit'}

# The keys of the dictionary provide the list of allowable keys:
allowed_keys = key_meanings.keys()

# %% Text stimuli

welcome_text = """Welcome to this experiment! 
- Press any key to continue -

P.S. If nothing happens, click somewhere on the screen and try again."""

instruction_text = "In this experiment you will play a game of matching pennies \
against the computer. In each round, please chose whether you want to present \
your penny heads-up or tails-up by pressing one of the following keys:\n" \
+ list(key_meanings.keys())[0] + " \u2192 heads-up \n" + list(key_meanings.keys())[1] + " \u2192 tails-up \n" + \
"""
If your choice matches the computer's choice, you win the round. If not, you lose the round.
There will be 10 rounds in total.

You can quit the game at any point by pressing the '""" + list(key_meanings.keys())[2] + """' key on the keyboard.

Ready to begin?

- Press any key to begin -
"""

trial_text = "Do you want to present your penny heads-up or tails-up?\n" + \
"Press '" + list(key_meanings.keys())[0] + "' \u2192 heads-up \n" + "Press '" + list(key_meanings.keys())[1] + \
"' \u2192 tails-up \n" + \
"\n" + "Press '" + list(key_meanings.keys())[2] + "' \u2192 quit the game"

# Prepare text for drawing in a window.
welcome = visual.TextStim(win, text=welcome_text, color='black', font='Arial', height=0.06, alignHoriz='center', pos=(0.5,0))
instruction = visual.TextStim(win, text=instruction_text, color='black', font='Arial', height=0.06, alignHoriz='center', pos=(0.5,0))
trial_start = visual.TextStim(win, text=trial_text, color='black', font='Arial', height=0.06, alignHoriz='center', pos=(0.5,0))
victory = visual.TextStim(win, text='YOU WON!', color='green', font='Arial', height=0.06, alignHoriz='center', pos=(0.5,0))
loss = visual.TextStim(win, text='YOU LOST.', color='red', font='Arial', height=0.06, alignHoriz='center', pos=(0.5,0))

# %% Image Stimuli

# Prepare image for drawing in a window.
heads_heads = visual.ImageStim(win, image='heads-heads.jpg')
heads_tails = visual.ImageStim(win, image='heads-tails.jpg')
tails_heads = visual.ImageStim(win, image='tails-heads.jpg')
tails_tails = visual.ImageStim(win, image='tails-tails.jpg')


# %% Intro screens

# Prepare the welcome text to be shown.
welcome.draw()
# 'Flip' the window to actually show the prepared text.
win.flip()

# Wait for a key press response.
event.waitKeys()

# Prepare and show the instruction text.
instruction.draw()
win.flip()

# Wait for a key response.
event.waitKeys()

# %% Run trials
score = 0 # starting score count 
choices = ['0'] # list of computer's choices
responses = ['0'] # list of participant's responses
keys = event.getKeys()

for trial in trials:
    # Show trial text asking the subject to make a response.
    trial_start.draw()
    win.flip()
    
    # Wait for a key press, allow only the previously specified keys.
    keys = event.waitKeys(keyList=allowed_keys)
    
    # Get the key that was pressed.
    key = keys[0]
    
    # Translate key into response.
    response = key_meanings[key]
    
    # Did the participant switch from his/her response in the previous trial?
    if responses[-1] == '0':
        ownswitch = '' # ignore first trial response
    elif response == responses[-1]:
        ownswitch = False
    else:
        ownswitch = True
    
    # Add response of current trial to list of all responses.
    responses.append(response)
    
    # Random choice made by the computer:
    outcomes = ['heads-up', 'tails-up'] # list of possible outcomes
    if strategy == 'no':
        choice = random.choices(outcomes, weights=(p_heads, p_tails), k=1)[0] # random/biased choice of outcomes
    elif strategy == 'yes':
        if choices[-1] == '0':
            choice = random.choices(outcomes, weights=(p_heads, p_tails), k=1)[0] # random/biased choice of outcomes in first trial
        elif choices[-1] == 'heads-up':
            choice = 'tails-up'
        elif choices[-1] == 'tails-up':
            choice = 'heads-up'

    # Did the participant switch from the computer's choice in the previous trial?
    if choices[-1] == '0':
        compswitch = '' # ignore first trial response/choice
    elif response == choices[-1]:
        compswitch = False
    else:
        compswitch = True
    
    # Add choice of current trial to list of all of the computer's choices.
    choices.append(choice)
    
    # Show the two pennies on the screen:
    if response == 'heads-up' and choice == 'heads-up':
        heads_heads.draw()
    elif response == 'quit': # Don't show pennies if subject presses 'q'
        break
    elif response == 'heads-up' and choice == 'tails-up':
        heads_tails.draw()
    elif response == 'tails-up' and choice == 'heads-up':
        tails_heads.draw()
    else:
        tails_tails.draw()
    win.flip()
    core.wait(1)
    
    # Show feedback depending on if the response matches the computer's choice:
    if response == choice:
        result = True
        score += 1 # update score
        victory.draw()
    elif response == 'quit': # No feedback if subject presses 'q'
        break
    else:
        result = False
        loss.draw()
    
    # Show current score:
    score_text = "Current score: %s" %(score)
    current_score = visual.TextStim(win, text=score_text, color='black', font='Arial', height=0.05, alignHoriz='center', pos=(0.5,-0.2))
    current_score.draw()
    win.flip()
    core.wait(1)
    
    # Save the subject's ID and responses into the TrialHandler object.
    trials.addData('ID', subj_id)
    trials.addData('Response', response)
    trials.addData('Choice', choice)
    trials.addData('Win', result)
    trials.addData('Score', score)
    trials.addData('CompSwitch', compswitch)
    trials.addData('OwnSwitch', ownswitch)
    

# %% End

# Show "Game Over" text on the screen
end_text = "Game Over"
end = visual.TextStim(win, text=end_text, color='black', font='Arial', height=0.06, alignHoriz='center', pos=(0.5,0))

end.draw()
win.flip()    

# Define a file name.
results_filename = subj_id + '.csv'

# Check whether it exists & use alternative name if necessary.
nr = 0
while os.path.isfile(results_filename):
    nr += 1
    # add '_nr' to filename if it already exists
    add_filename = (lambda x: subj_id + '_' + str(x) + '.csv')
        # note: lambda functions are subject to a more restrictive but more concise syntax than regular Python functions
    results_filename = add_filename(nr + 1) # increase the nr by 1 (it will effectively start at '_2')
    continue # repeat procedure until new, not yet existing file(name) is found

# Printout of the results to file.
results = trials.saveAsWideText(results_filename, matrixOnly=False)

# Clean up printout.
# adapted from: https://stackoverflow.com/questions/7588934/how-to-delete-columns-in-a-csv-file
f = pandas.read_csv(results_filename) # reads created file
keep_col = ['ID', 'TrialNumber', 'Response', 'Choice', 'Win', 'Score', 'CompSwitch', 'OwnSwitch'] # select columns to keep
new_f = f[keep_col] # limits content to selection
new_f.to_csv(results_filename, index=False) # replaces file with selected content only

# Close the window.
win.close()

# %% Summary

# Calculate switches from previous response.
own_switch = 0 # baseline count of switches from own previous response

subj_data = pandas.read_csv(results_filename) # read experiment data from the created file
response_list = subj_data.Response.tolist() # create list of subject's responses

own_switch = Kind_Assignment_Functions.count_prev_switches(response_list, response_list, t_nr) # calculate switches

    
# Calculate switches from previous choice made by the computer.
comp_switch = 0 # baseline count of switches from computer's previous response

choice_list = subj_data.Choice.tolist() # create list of computer's choices

comp_switch = Kind_Assignment_Functions.count_prev_switches(response_list, choice_list, t_nr) # calculate switches


# Append participant file with this data.
row_total = ['Total score: ', score]
row_own_switches = ['Switches from own response: ', own_switch]
row_comp_switches = ["Switches from computer's choice: ", comp_switch]

Kind_Assignment_Functions.append_list_as_row(results_filename, '')
Kind_Assignment_Functions.append_list_as_row(results_filename, row_total)
Kind_Assignment_Functions.append_list_as_row(results_filename, row_own_switches)
Kind_Assignment_Functions.append_list_as_row(results_filename, row_comp_switches)
Kind_Assignment_Functions.append_list_as_row(results_filename, '')

# Response statistics print-out to console
print("SUBJECT ", subj_id)
print("Total score: ", score)
print("Times switched from own previous response: ", own_switch)
print("Times switched from computer's previous response: ", comp_switch)

