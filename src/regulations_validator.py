#!/usr/bin/env python
import sys, os, os.path, tempfile

"""
This program is a validator
"""


def file_length_checker(file_name):
    """
    Checks the length of the file returned to the validator
    :param file_name: path of the file to be checked
    :return:
    """
    result = open(file_name, "r")
    counter = 0
    for line in result:
        counter += 1
    return counter <= 1000


def documents_checker(path):
    """
    Checks the names of the files returned from the documents jobs
    :param path: location of the results files from the job
    :return:
    """
    file_name = get_file_name(path)
    number = True
    for x in range(7,10):
        try:
            file_name[x].isdigit()
            int(file_name[x])
        except:
            number = False
            break

    if file_name.startswith("results") and number and file_name.endswith(".txt"):
        if file_length_checker(path):
            return 1
    else:
        return 0


def document_checker(path):
    """
    Checks the files returned from the document job
    :param path: location of the result files
    :return:
    """
    file_name = get_file_name(path)
    split_id = file_name.split("-")
    split_id = split_id[len(split_id) - 1].split(".")
    document_number = split_id[len(split_id) - len(split_id)]
    if file_name.startswith("doc.") and int_checker(document_number):
        return 1
    else:
        return 0


def int_checker(string):
    """
    This is a private function used to check to see if the string passed is an int
    :return:
    """
    for x in range(len(string)):
        try:
            int(string[x])
        except:
            return False
    return True


def get_file_name(path):
    """
    Extracts the name of the file from the given path
    :param path: location of the file in which the name will be extracted from
    :return:
    """
    split_path = path.split("/")
    file_name = split_path[len(split_path) - 1]
    return file_name


if __name__ == "__main__":
    if sys.argv[1] != '--error':

        tar_file = sys.argv[1]
        PATH = tempfile.mkdtemp()
        PATHstr = str(PATH)

        # Unzip the tar file and then remove the tar file
        os.system("tar xzf " + tar_file + " --directory " + PATHstr)

        # Create a list of all the files in the directory
        file_list = os.listdir(PATHstr)

        count = 0

        for file in file_list:

            count += documents_checker(PATHstr + "/" + file)
            count += document_checker(PATHstr + "/" + file)

        if os.path.exists(PATHstr + '/job_id.txt'):
            count += 1

        if count == len(file_list):
            sys.exit(0)

        else:
            sys.exit(1)
