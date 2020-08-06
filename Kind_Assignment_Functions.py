# -*- coding: utf-8 -*-
"""
Author: Elisabeth Kind

Module defining functions for the 'Matching pennies' assignment program
"""

import pandas

import csv
from csv import writer

# %% Function 1

def count_prev_switches(list_trial, list_prev, t_nr):
    """
    Function (generator) that generates how many times a subject switched its response
    compared to a response in the previous trial
    
    Example:
        >>> count_prev_switches(response_list, response_list)
        9

    Parameters
    ----------
    list_trial : LIST
        list of responses in a variable per trial - e.g. list of all of the subject's responses
    list_prev : LIST
        list of responses in a variable per trial which you want to compare responses to\
        (if you are interested in switches between one's own response in a previous trial \
        this may be the same as list_trial) - e.g. list of all of the subject's responses
    t_nr : INTEGER
        number of trials in the experiment - e.g. 10
    EXCEPTIONS: 
        None

    Returns
    -------
    count : INTEGER 
        integer specifying how many times the response was switched - e.g. 8
    """

    count = 0
    list_trial = list_trial[-t_nr:]
    list_prev = list_prev[-t_nr:]
    
    for x, item in enumerate(list_trial):
        if x > 0:
            if list_trial[x] != list_prev[x-1]:
                count += 1 # increase count by 1 if difference btw. current and last trial response
            else:
                continue
    count -= 1 # subtract 1 to ignore comparison of first trial response
    return count

# %% Function 2
    
def append_list_as_row(file_name, list_of_elem):
    # adapted from: https://thispointer.com/python-how-to-append-a-new-row-to-an-existing-csv-file/
    """
    Function that adds a new row to an existing csv file.
    
    Example:
        >>> append_list_as_row('test.csv', ['add this as new row', 'next column'])
        
    Parameters
    ----------
    file_name : FILENAME of existing csv file
        name of the file you want to add a new row to at the end - e.g. 'test.csv'
    list_of_elem : LIST
        content of the row you want to add (each list element will be in new column)\
        - e.g. ['add this as new row', 'next column']
    EXCEPTIONS:
        None

    Returns
    -------
        None
    """
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
        

# %% Test

# Function 1
if __name__ == '__main__':
    results_filename = 'test.csv'
    subj_data = pandas.read_csv(results_filename)
    response_list = subj_data.response.tolist()
    t_nr = 10
    print('Switches: ' + str(count_prev_switches(response_list, response_list, t_nr)))


# Function 2
if __name__ == '__main__':   
    file_name = 'test.csv'
    list_of_elem = ['add', 'me']
    append_list_as_row(file_name, list_of_elem)
    
    with open(file_name,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        data = list(reader)
        row_count = len(data) # find nr of rows in file
    df = pandas.read_csv(file_name, skiprows = row_count - 1) # read last row of file
    print(df) # print this last row
