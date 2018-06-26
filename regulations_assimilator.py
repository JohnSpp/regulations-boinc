#!/usr/bin/env python

import sys, os, os.path, subprocess

"""
This program does the assimilation for Boinc. 
It creates a master file of squares and adds the results of all of the work to the file.
:return:
"""

def checkFile(filePath):
        """
        Simple checker to see if the file needs to be created or appended to.
        """

        if os.path.exists(filePath): 
                append_write = 'a'
        else: 
                append_write = 'w'

        return append_write

if sys.argv[1]!='--error':

        masterS = "/root/project/bin/mastersquare.csv" 
        masterC = "/root/project/bin/mastercube.csv" 

        os.system("tar xzf " + str(sys.argv[1]))

        if os.path.exists("cubes.txt"):
                print("It was a cube file")

                master = open(masterC, checkFile(masterC))

                result = open("cubes.txt", "r")
                for line in result:
                        master.write(line)

                result.close()
                master.close()
        
        elif os.path.exists("output.txt"):
                print("It was a square file")

                master = open(masterS, checkFile(masterS))

                result = open("output.txt", "r")
                for line in result:
                        if int(line) == 4:
                                os.system("python /root/project/bin/test_cube.py 1")
                        master.write(line)

                result.close()
                master.close()

        else:
                print("We got something else") 
        
