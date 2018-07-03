from documents_processor import *
import tempfile
import mock


import pytest
import requests_mock

from api_call import *

home = os.getenv("HOME")
with open(home + '/.env/regulationskey.txt') as f:
    key = f.readline()
base_url = 'https://api.data.gov:443/regulations/v3/documents.json?'


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture()
def workfile_tempdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@mock.patch('documents_processor.get_sys_arg', return_value='1234567891011121')
def test_documents_processor(patch, mock_req, workfile_tempdir):
    mock_req.get('http://10.76.100.145:5000/get_data?job_id=1234567891011121', status_code=200, text=base_url)
    mock_req.get(base_url, status_code=200, text='{"documents": '
                                                              '[{"documentId": "CMS-2005-0001-0001", "attachmentCount": 4},\
                                                                {"documentId": "CMS-2005-0001-0002", "attachmentCount": 999}]}')
    result = documents_processor(workfile_tempdir)
    assert result

@mock.patch('documents_processor.get_sys_arg', return_value='1234567891011121')
def test_valid_results(mock_req, workfile_tempdir):
    mock_req.get(base_url, status_code=200, text='{"documents": '
                                                              '[{"documentId": "CMS-2005-0001-0001", "attachmentCount": 4},\
                                                                {"documentId": "CMS-2005-0001-0002", "attachmentCount": 999}]}')
    result = process_results(process_call(add_api_key(base_url)), workfile_tempdir)
    assert result


def test_successful_call(mock_req):
    mock_req.get(base_url, status_code=200, text='{}')
    assert process_call(base_url).text == '{}'


def test_call_fail_raises_exception(mock_req):
    mock_req.get(base_url, status_code=407, text='{}')
    with pytest.raises(CallFailException):
        process_call(base_url)


def test_empty_json(mock_req):
    mock_req.get(base_url, status_code=200, text='')
    with pytest.raises(BadJsonException):
        process_results(process_call(base_url), "")


def test_bad_json_format(mock_req):
    mock_req.get(base_url, status_code=200, text='{information: [{},{}]}')
    with pytest.raises(BadJsonException):
        process_results(process_call(base_url), "")





