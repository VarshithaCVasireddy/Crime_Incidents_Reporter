import pytest
import os
import io
import sqlite3

import project0


@pytest.fixture
def sample_incident_file():
    cwd = os.getcwd()
    return os.path.join(cwd, 'tests', 'sample.pdf')


def test_fetchincidents(sample_incident_file):
    file_data = project0.fetchincidents('file://' + sample_incident_file)
    assert isinstance(file_data, bytes)


def test_extractincidents(sample_incident_file):
    with open(sample_incident_file, 'rb') as sample_fp:
        data = project0.extractincidents(sample_fp.read())

        assert len(data) == 237


def test_createdb():
    db_name = project0.createdb()
    db_path = os.path.join(os.getcwd(), db_name)

    assert os.path.exists(db_path) is True

    connection = sqlite3.connect(db_name)
    assert connection.total_changes == 0

    os.remove(db_path)


def test_populatedb():
    incidents = [
        ['2/24/2022 20:17', '2022-00003512', '1518 MORREN DR', 'Sick Person', 'EMSSTAT'],
        ['2/24/2022 20:17', '2022-00003514', '1518 MORREN DR', 'Sick Person', 'EMSSTAT'],
        ['2/24/2022 18:01', '2022-00003507', '', '', 'EMSSTAT']
    ]

    db_name = project0.createdb()
    db_path = os.path.join(os.getcwd(), db_name)
    change_count = project0.populatedb(db_name, incidents)

    assert change_count == len(incidents)

    os.remove(db_path)


def test_status():
    incidents = [
        ['2/24/2022 20:17', '2022-00003512', '1518 MORREN DR', 'Sick Person', 'EMSSTAT'],
        ['2/24/2022 20:17', '2022-00003514', '1518 MORREN DR', 'Sick Person', 'EMSSTAT'],
        ['2/24/2022 18:01', '2022-00003507', '', '', 'EMSSTAT']
    ]

    db_name = project0.createdb()
    db_path = os.path.join(os.getcwd(), db_name)
    project0.populatedb(db_name, incidents)

    actual = project0.status(db_name)
    expected = 'Sick Person|2'

    assert expected in actual

    os.remove(db_path)
