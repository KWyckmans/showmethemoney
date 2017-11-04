import os
import datetime

import unittest
import money


class MoneyTest(unittest):
    def statement_file(tmpdir_factory):
        temp_file = tmpdir_factory.mkdir("statements").join("statements.csv")
        temp_file.write("test,20160101,200.12")
        temp_file.write("test,20160101,-100")

        return temp_file


    def test_statement_initializes():
        statement = money.Statement(description="Carrefour",
                                    amount=20.32, timestamp=datetime.datetime.now(), recipient="Carrefour")

        assert statement.description == "Carrefour"

    def test_load_statements_from_file():
        parser_factory = money.StatementParserFactory()
        parser = parser_factory.create_parser('ing')
        money.STATEMENTS = parser.parse(statement_file)

        assert len(money.STATEMENTS) > 0