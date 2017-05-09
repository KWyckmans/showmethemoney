'''
Parses and processes ING statement csv files.
'''

import csv

class Statement(object):
    '''The Statement class represents a single entry from your bank statements

    A statement contains:
    - Description: what the transaction was about
    - Amount: Amount of money received or transferred,
    - Timestamp: The date of the transaction
    '''
    def __init__(self, description, amount, timestamp):
        self.description = description
        self.amount = amount
        self.timestamp = timestamp


def main():
    pass

if __name__ == '__main__':
    main()
