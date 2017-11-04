"""
Parses and processes ING statement csv files.
"""

import csv
import datetime
import glob

import re
import logging


class IngStatementParser(object):
    def __init__(self):
        pass

    def parse(self, statement_file):
        with open(statement_file) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                if row['Bedrag'] is not '':
                    description = ' '.join(row['Omschrijving'].split())

                    description = self.__strip_amount_from_detail(description)
                    description = self.__strip_date_from_detail(description)
                    description = self.__strip_hour_from_detail(description)
                    if self.__is_visa_statement(description):
                        description = 'VISA Payment'
                    else:
                        parts = description.split('-')
                        description = parts[0]
                        if len(parts) > 2:
                            description = description + parts[2]
                            description_extra = ' '.join(parts[3:])
                            recipient = self.__extract_pre_country_details(description_extra)
                            country = self.__extract_country_code(description_extra)

                    description = ' '.join(row['Omschrijving'].split())

                    yield Statement(description, float(row['Bedrag'].replace(',', '.')),
                                    datetime.datetime.strptime(row['Boekingsdatum'], "%d/%m/%Y"),
                                    row['Rekening tegenpartij'],
                                    Account(row['Naam van de rekening'], row['Rekeningnummer']), row['Munteenheid'],
                                    ' '.join(row['Detail van de omzet'].split()), ' '.join(row['Bericht'].split()))

    @staticmethod
    def __extract_country_code(detail):
        match_country = re.search('\s[A-Z][A-Z][A-Z]\s', detail)
        if match_country:
            start = match_country.span()[0] + 1
            end = match_country.span()[1] - 1
            return detail[start:end]
        else:
            return ''


    @staticmethod
    def __extract_pre_country_details(detail):
        data = re.split('\s[A-Z][A-Z][A-Z]\s', detail)
        return data[0]

    @staticmethod
    def __strip_hour_from_detail(detail):
        date = re.split('[0-9]+.[0-9]+ uur', detail)
        return ' '.join(date)

    @staticmethod
    def __strip_date_from_detail(detail):
        date = re.split('[0-9]+/[0-9]+', detail)
        return ' '.join(date)

    @staticmethod
    def __strip_amount_from_detail(detail):
        amount = re.split('- [0-9]+,[0-9]+', detail)
        return ' '.join(amount)

    @staticmethod
    def __is_visa_statement(detail):
        if detail.startswith('BCC-ING'):
            return True

        return False

    def __convert_visa_detail(self, detail):
        pass


class StatementParserFactory(object):
    def __init__(self):
        pass

    def create_parser(self, parser_type):
        if parser_type == 'ing':
            return IngStatementParser()
        else:
            raise NotImplementedError('No such parser exists')


class Account(object):
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f'{self.name} - {self.number}'


class Statement(object):
    def __init__(self, description, amount, timestamp, recipient, account, currency='Eur', details='', message=''):
        self.description = description
        self.amount = amount
        self.timestamp = timestamp
        self.recipient = recipient
        self.account = account
        self.currency = currency
        self.details = details
        self.message = message

    def __str__(self):
        return f'''{abs(self.amount)} ({self.currency}) | {self.recipient} | {self.description} | {self.timestamp} | {self.account} | {self.details} | {self.message}'''


def get_years(statements):
    return {statement.timestamp.year for statement in statements}


def get_months(statements):
    return {statement.timestamp.month for statement in statements}


def get_statements_grouped_per_year_and_month(statements, years, months):
    grouped_statements = {year: {month: [] for month in months} for year in years}

    for year in years:
        for month in months:
            logging.debug("Collecting statements for %s - %s", year, month)
            grouped_statements[year][month] = \
                [
                    statement for statement in statements
                    if statement.timestamp.year == year
                       and statement.timestamp.month == month
                ]

    return grouped_statements


def main():
    logging.basicConfig(format='%(asctime)-15s %(funcName)s %(levelname)s %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    statements = []
    for file in glob.glob("*.csv"):
        logger.info("Processing file %s", file)
        statements.extend(StatementParserFactory().create_parser('ing').parse(file))

    years = get_years(statements)
    months = get_months(statements)
    grouped_statements = get_statements_grouped_per_year_and_month(statements, years, months)

    for statement in grouped_statements[2016][1]:
        logger.debug(statement)

if __name__ == '__main__':
    main()
