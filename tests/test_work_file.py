import pytest
import tempfile
import os

import work_file as wf


@pytest.fixture()
def workfile_tempdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def create_work_file(num, workfile_tempdir):
    test_txt = workfile_tempdir + str("{:0>4d}").format(num) + ".txt"
    wf.work_file(test_txt)
    return test_txt


def test_new_work_file_size():
    create_work_file(0, "")
    wf.work_file("")
    assert wf.size() == 0


def test_add_doc_changes_size():
    create_work_file(0, "")
    wf.work_file("")
    wf.add_doc("ID", 1)
    assert wf.size() == 1


def test_write_creates_file(workfile_tempdir):
    test_txt = create_work_file(0, workfile_tempdir)
    wf.write()
    assert os.path.exists(test_txt)


def test_write_check_content(workfile_tempdir):
    test_txt = create_work_file(0, workfile_tempdir)
    wf.add_doc("ID", 1)
    wf.add_doc("ID", 2)
    wf.add_doc("ID", 3)
    wf.write()
    with open(test_txt, 'r') as f:
        assert f.readline().strip() == "ID,1"


def test_write_many_ids(workfile_tempdir):
    test_txt = create_work_file(0, workfile_tempdir)
    number = 1000000
    for x in range(number):
        wf.add_doc("ID", 1)
    wf.write()
    with open(test_txt, 'r') as f:
        assert f.readline().strip() == "ID,1"
