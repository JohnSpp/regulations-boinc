#!/usr/bin/env python

import sys, os, os.path, tempfile, requests, re, shutil

from doc_work_gen import build_job

ip = "http://10.76.100.145:5000"

server_key = os.environ["WORK_SERVER_KEY"]

"""
This program does the assimilation for Boinc. 
It creates a master file of squares and adds the results of all of the work to the file.
:return:
"""


def documents_job(path):
    """
    This reads the file given at path
    Makes a list of all document ids
    Builds a job from the document ids
    :param path: location of the file which contains the document ids
    :return:
    """
    document_ids = []
    with open(path, 'r') as f:
        for line in f:
            doc_id = line.strip()
            document_ids.append(doc_id)
    build_job(document_ids)


def document_job(path):
    """
    Saves the data from the file given at path
    :param path: location of the file which contains the information about a document
    :return:
    """
    save_path = 'root/project/data/'
    local_save(path, save_path)
    # TODO: Save it to Google Storage


def get_file_name(path):
    """
    Extracts the name of the file from the given path
    :param path: location of the file in which the name will be extracted from
    :return:
    """
    split_path = path.split("/")
    file_name = split_path[len(split_path) - 1]
    return file_name


def get_document_id(file_name):
    """
    Extract the document id from the file name
    :param file_name: name of the file that the id will be extracted from
    :return id: the string of the document id from the file name
    """
    doc,id,ending = file_name.split(".")
    return id


def create_new_dir(path):
    """
    If the path does not exist, create the directory
    :param path: the path to the directory to be created
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_doc_attributes(file_name):
    """
    Get the organization(s), the docket_id and the document_id from a file name
    :param file_name: name of the file to extract attributes of the document name
    :return:
    """
    document_id = get_document_id(file_name)
    split_name = re.split("[-_]", document_id)
    org = split_name[0]
    org_num = 1
    if not split_name[1].isdigit():
        org = org + '-' + split_name[1]
        org_num = 2
    docket_id = split_name[0]
    for name in split_name[org_num:-1]:
        docket_id += '-' + name
    document_id = docket_id + '-' + split_name[-1]
    return org, docket_id, document_id


def local_save(cur_path, destination):
    """
    Save the file located at the current path to the destination location
    :param cur_path: location of the file to be saved
    :param destination: location that the file should be saved
    :return:
    """
    file_name = get_file_name(cur_path)
    org, docket_id, document_id = get_doc_attributes(file_name)
    destination_path = destination + org + "/" + docket_id + "/" + document_id + "/"
    create_new_dir(destination_path)
    shutil.copy(cur_path, destination_path + '/' + file_name)


def remove_job(path):
    """
    Communicates with the work server to remove completed jobs
    :param path: location of the files to retrieve the job id
    :return:
    """
    with open(path + 'job_id.txt', 'r') as f:
        job_id = f.read().strip()
    r = requests.post(ip + "/work_done", data=dict(job_id=job_id, key=server_key))
    r.raise_for_status()


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

            # Documents Checker
            if file.startswith("results"):
                documents_job(PATH + "/" + file)

            # Document Checker
            elif file.startswith("doc."):
                document_job(PATH + "/" + file)

        remove_job(PATH)