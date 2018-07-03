
total_size = 0
document_ids = []
filename = ""
counts = []


def work_file(file_path):
    """
    Constructor for the work file
    Sets all of the global variables to their initial states
    :param file_path: this is the path where the file is that will be written to
    :return:
    """
    global filename, document_ids, total_size, counts
    filename = file_path
    document_ids = []
    total_size = 0
    counts = []


def write():
    """
    This function creates the file given and writes all of the document ids in the work file
    :return:
    """
    with open(filename, 'w+') as f:
        for i, doc_id in enumerate(document_ids):
            f.write(doc_id + "," + counts[i] + "\n")


def add_doc(document_id, count):
    """
    This adds the document id to the list of ids that will be saved to a file
    The count is the number of calls necessary to collect all of the data for the specific document id
    :param document_id: the document id as a string
    :param count: this is an integer for the number of calls to collect all information about the given document
    :return:
    """
    global total_size, counts
    total_size += count
    document_ids.append(document_id)
    counts.append(str(count))


def size():
    """
    :return: this returns the total number of requests necessary to collect all of the
    data from all the current document ids
    """
    return total_size




