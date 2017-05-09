'''
Parses and processes ING statement csv files.
'''
import datetime
import csv

STATEMENTS = []

def statement_file(statement_file):
    yield Statement('you',0,datetime.datetime.now(),'me')

class IngStatementParser(object):
    '''Parses statement files from the Belgian ING Bank'''
    def __init__(self):
        pass

    def parse(self, statement_file):
        '''Parses a csv file containing statements'''
        return [Statement('test', 0, datetime.datetime.now(), 'me')]

class StatementParserFactory(object):
    def __init__(self):
        pass

    def create_parser(self, type):
        return IngStatementParser()


class Statement(object):
    '''The Statement class represents a single entry from your bank statements

    A statement contains:
    - Description: what the transaction was about
    - Amount: Amount of money received or transferred,
    - Timestamp: The date of the transaction
    '''
    def __init__(self, description, amount, timestamp, recipient):
        self.description = description
        self.amount = amount
        self.timestamp = timestamp
        self.recipient = recipient

def main():
    STATEMENTS.extend(StatementParserFactory().create_parser('ing').parse(''))

    for statement in statement_file(None):
        print(statement.description)

if __name__ == '__main__':
    main()
