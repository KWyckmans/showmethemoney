import os
import datetime

import pytest
import money


@pytest.fixture(scope='session')
def statement_file(tmpdir_factory):
    temp_file = tmpdir_factory.mkdir("statements").join("statements.csv")
    temp_file.write("test,20160101,200.12")
    temp_file.write("test,20160101,-100")

    return temp_file


def test_statement_initializes():
    statement = money.Statement(description="Carrefour",
                                amount=20.32, timestamp=datetime.datetime.now(), recipient="Carrefour")

    assert statement.description == "Carrefour"
