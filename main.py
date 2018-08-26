import getpass
from datetime import datetime

import keyring

from gspreadsheet import GSpreadSheet
from jiraTimeAggregator import JiraTimeAggregator

JIRA_URL = 'https://jira.billing.ru'
JIRA_USER = 'dmitrii.sulimchuk'

SPREADSHEET_ID = '15_wNVfvgObDtTTwFY5Ta6677bU6mn3lY8xGbdy1osZc'
READ_RANGE_NAME = 'Лист1!B2:C2'
APPEND_RANGE_NAME = 'Лист1!B6:C'


def main():
    jira_client = init_jira()

    gservice = GSpreadSheet(SPREADSHEET_ID, READ_RANGE_NAME, APPEND_RANGE_NAME)
    query = gservice.read_range()[0]
    print(query)

    result = jira_client.query(query[1])
    print(result)
    time = str(datetime.now())
    data = [time, result['originalEstimate'], result['timespent']]
    print("Try to append: ", data)
    gservice.append(data)


def init_jira():
    jira_password = keyring.get_password(JIRA_URL, JIRA_USER)
    if jira_password is None:
        jira_password = getpass.getpass()
        print(jira_password)
        jira_client = JiraTimeAggregator(JIRA_URL, JIRA_USER, jira_password)
        keyring.set_password(JIRA_URL, JIRA_USER, jira_password)
        return jira_client
    jira_client = JiraTimeAggregator(JIRA_URL, JIRA_USER, jira_password)
    return jira_client


if __name__ == '__main__':
    main()
