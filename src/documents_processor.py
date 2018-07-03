from api_call_managment import *
import work_accumulator as wa
import sys
import json

base_url = 'http://10.76.100.145:5000/get_data?job_id='

home = os.getenv("HOME")
with open(home + '/.env/regulationskey.txt') as f:
    key = f.readline()


def documents_processor(dirpath):
    """
    Open the file found at file path
    For each line in the file, make the appropriate api call
    Process the results from the api call to generate work files
    :param dirpath: path of the directory where workfiles will be written
    :return: returns True if the processor completed successfully
    """
    job_id = get_sys_arg()

    get_call = base_url + job_id
    urls = process_call(get_call)

    for url in urls:
        result = process_call(add_api_key(url.decode('utf-8')))
        process_results(result, dirpath)

    with open(dirpath + "/job_id.txt", "w+") as j:
        j.write(job_id)

    return True


def process_call(url):
    """
    Uses the api call manager to get the information
    :param url: the url that will be called using the api
    :return: returns the result of the api call
    """
    result = api_call_manager(url)
    return result


def process_results(result, dirpath):
    """
    Loads the json from the results of the api call
    Gets the list of documents from the json
    Create a new work accumulator that organizes the documents returned from each api call
    :param result: Result of the api call
    :param dirpath: path of the directory where workfiles will be written
    :return: returns True if the processing completed successfully
    """
    docs_json = load_json(result)
    try:
        doc_list = docs_json["documents"]
    except TypeError:
        raise BadJsonException
    wa.work_accumulator(dirpath)
    for doc in doc_list:
        doc_id = doc["documentId"]
        calls = doc["attachmentCount"] + 1
        wa.add_doc(doc_id, calls)
    wa.terminate()
    return True


def load_json(result):
    """
    loads the json format from the result of the api call
    :param result: the result of the api call
    :return: returns the json format of the api call
    """
    try:
        docs_json = json.loads(result.text)
    except json.JSONDecodeError:
        raise BadJsonException
    return docs_json

def get_sys_arg():
    """
    Gets the command line argument
    :return: the argument given in the command line
    """
    return sys.argv[1]


# Raised if the json is not correctly formatted or is empty
class BadJsonException(Exception):
    print("NOTICE: The Json appears to be formatted incorrectly.")
