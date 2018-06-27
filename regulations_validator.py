#!/usr/bin/env python
import sys, os, os.path

"""
This program is a trivial validator that always passes.
This shows where the standard validation happens within the program.
"""


def file_length_checker(fileName):
    
    result = open(fileName, "r")
    counter = 0

    for line in result:
        counter += 1

    return counter <= 1000


if sys.argv[1]!='--error':

    tar_file = str(sys.argv[1])

    os.system("tar xzf " + tar_file + "; rm " + tar_file)

    file_list = os.listdir(os.path.dirname(os.path.abspath(__file__))) 

    counter = 0

    for file in file_list:

        if file.startswith("results"):
            if file_length_checker(file):
                counter += 1
            else:
                pass

        elif file.startswith("doc.") and (file.endswith(".json") or file.endswith(".html") or file.endswith(".pdf") or file.endswith(".tiff")):
            counter += 1

        else:
            pass

    if counter == len(file_list):
        sys.exit(0)

    else:
        sys.exit(1) 
        