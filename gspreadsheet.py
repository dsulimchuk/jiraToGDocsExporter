from __future__ import print_function

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def init_credentials():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', 'https://www.googleapis.com/auth/spreadsheets')
        creds = tools.run_flow(flow, store)
    return creds


class GSpreadSheet:

    def __init__(self, spreadsheet, read_range_name, append_range_name) -> None:
        self.spreadsheet = spreadsheet
        self.read_range_name = read_range_name
        self.append_range = append_range_name
        creds = init_credentials()
        self.service = build('sheets', 'v4', http=creds.authorize(Http()))

    def append(self, data):
        self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheet,
                                                    range=self.append_range,
                                                    valueInputOption="USER_ENTERED",
                                                    body={'values': [data]}
                                                    ).execute()

    def read_range(self):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet,
                                                          range=self.read_range_name,
                                                          ).execute()
        values = result.get('values', [])
        return values


if __name__ == '__main__':
    # test data
    SPREADSHEET_ID = '15_wNVfvgObDtTTwFY5Ta6677bU6mn3lY8xGbdy1osZc'
    READ_RANGE_NAME = 'Лист1!B2:C2'
    APPEND_RANGE_NAME = 'Лист1!B6:C'

    g_spread_sheet = GSpreadSheet(SPREADSHEET_ID, READ_RANGE_NAME, APPEND_RANGE_NAME)
    values = g_spread_sheet.read_range()

    if not values:
        raise Exception('empty')
    else:
        for row in values:
            print(row)
            # return row[1]

    idx = 0
    while idx < 4:
        g_spread_sheet.append([idx])
        idx += 1
