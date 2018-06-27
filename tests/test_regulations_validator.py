import pytest, os, tempfile

import regulations_validator as rv


# two parameters, the validator/assimilator being used and the zip file of what it is receiving


def test_new_work_validator():
    assert rv.run('~/regulations-boinc/regulations-boinc/zip.tar.gz') == 0
