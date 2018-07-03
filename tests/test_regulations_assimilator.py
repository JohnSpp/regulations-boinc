import pytest
import requests_mock
import tempfile
import os

import regulations_assimilator as ra

PATH = 'test_files/'

@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture()
def workfile_tempdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture()
def savefile_tempdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_get_document_id():
    assert ra.get_document_id('doc.mesd-2018-234234-0001.json') == "mesd-2018-234234-0001"


def test_get_document_id_special():
    assert ra.get_document_id('doc.AHRQ_FRDOC_0001-0036.json') == "AHRQ_FRDOC_0001-0036"


def test_get_file_name():
    assert ra.get_file_name(PATH + 'doc.mesd-2018-234234-0001.json') == "doc.mesd-2018-234234-0001.json"


def test_create_new_dir(workfile_tempdir):
    ra.create_new_dir(workfile_tempdir)
    assert os.path.exists(workfile_tempdir)


def test_get_doc_attributes():
    org, docket, document = ra.get_doc_attributes('doc.mesd-2018-234234-0001.json')
    assert org == "mesd"
    assert docket == "mesd-2018-234234"
    assert document == "mesd-2018-234234-0001"


def test_get_doc_attributes_special():
    org, docket, document = ra.get_doc_attributes('doc.mesd_2018_234234-0001.json')
    assert org == "mesd"
    assert docket == "mesd-2018-234234"
    assert document == "mesd-2018-234234-0001"


def test_local_save(workfile_tempdir, savefile_tempdir):
    filename = 'doc.mesd_2018_234234-0001.txt'
    path = workfile_tempdir + '/' + filename
    with open(path, 'w') as f:
        f.write("Stuff was written here")
    org, docket_id, document_id = ra.get_doc_attributes(filename)
    ra.local_save(path, savefile_tempdir + '/')
    assert os.path.exists(savefile_tempdir + '/' + org + '/' + docket_id + '/' + document_id + '/' + filename)



