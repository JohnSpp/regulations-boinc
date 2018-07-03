from documents_processor import *

base_url = 'https://api.data.gov/regulations/v3/document?documentId='
server_url = 'https://10.76.100.164:5000/'


def document_processor(dirpath):
    """
    This will read document Ids from a file located at filepath
    For each document an api call will be made and the content will be downloaded and saved into dirpath
    :param dirpath: path to the directory where the downloads will be saved
    :return:
    """
    job_id = get_sys_arg()
    get_call = server_url + job_id
    doc_ids = process_call(get_call)

    for doc_id in doc_ids:
        result = process_call(add_api_key(make_doc_url(doc_id)))
        total = get_extra_documents(result, dirpath, doc_id)
    with open(dirpath + "/documents.txt", "w+") as wr:
        wr.write("This is a response from a Document Job")
    with open(dirpath + "/job_id.txt", "w+") as j:
        j.write(job_id)

def make_doc_url(documentId):
    """
    Given a documentID as a string append it to the end of the api call
    :param documentId: the string of a documentId
    :return:
    """
    return base_url + documentId


def save_document(dirpath, doc_json, documentId):
    """
    Saves the json of the document call
    :param dirpath: path to the directory where the json will be saved
    :param doc_json: the json recieved from the api call
    :param documentId: the string of a documentId
    :return:
    """
    with open(dirpath + "/doc." + documentId + ".json" , "w+") as f:
        json.dump(doc_json, f)


def download_document(dirpath, documentId, result, type):
    """
    Saves the other file formats of the document call
    :param dirpath: path to the directory where the download will be saved
    :param documentId: the string of a documentId
    :param result: the result received from the api call
    :param type: the type of file that will be saved
    :return:
    """
    # These are special cases where the api representation is different from the user's
    if(type == "excel12book"):
        type = "xlsx"
    if(type == "msw12"):
        type = "doc"
    with open(dirpath + "/doc." + documentId + "." + type, 'wb') as f:
        for chunk in result.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def get_extra_documents(result, dirpath, documentId):
    """
    Download the json of the result from the original api call
    Determine if the document has additional formats that need to be downloaded
    Determines if the document has attachments that need to be downloaded
    :param result: the result of the api call
    :param dirpath: path to the directory where the download will be saved
    :param documentId: the string of a documentId
    :return: the total number of requests required to download all of them
    """
    doc_json = load_json(result)
    save_document(dirpath, doc_json, documentId)
    total_requests = 0
    total_requests += download_doc_formats(dirpath, doc_json, documentId)
    total_requests += download_attachments(dirpath, doc_json, documentId)
    return total_requests


def download_doc_formats(dirpath, doc_json, documentId):
    """
    Download the other formats for the document
    :param dirpath: path to the directory where the download will be saved
    :param doc_json: the json from a single document api call
    :param documentId: the string of a documentId
    :return:
    """
    total_requests = 0
    try:
        extra_formats = doc_json["fileFormats"]
        total_requests += len(extra_formats)
        for extra_doc in extra_formats:
            result = process_call(add_api_key(str(extra_doc)))
            here = extra_doc.index("contentType") + 12
            type = extra_doc[here:]
            download_document(dirpath, documentId, result, type)
    except KeyError:
        pass
    return total_requests


def download_attachments(dirpath, doc_json, documentId):
    """
    Download the other attachments for the document
    :param dirpath: path to the directory where the download will be saved
    :param doc_json: the json from a single document api call
    :param documentId: the string of a documentId
    :return:
    """
    total_requests = 0
    try:
        extra_attachments = doc_json["attachments"]
        total_requests += len(extra_attachments)
        for attachment in extra_attachments:
            attachment_formats = attachment["fileFormats"]
            for a_format in attachment_formats:
                here = str(a_format).index("contentType") + 12
                type = str(a_format)[here:]
                result = process_call(add_api_key(str(a_format)))
                download_document(dirpath, documentId, result, type)
    except KeyError:
        pass
    return total_requests






