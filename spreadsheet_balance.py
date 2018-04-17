import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
sheet = client.open('Balance').sheet1
pp.pprint(sheet.row_values(3))


def change_order(first_row, last_row):
    for i in range(first_row, last_row + 1):
        values_last_row = sheet.row_values(last_row)
        sheet.insert_row(values_last_row, i)
        sheet.delete_row(last_row + 1)


class Person:
    def __init__(self, name, column_index, latest_value):
        self.name = name
        self.column_index = column_index
        self.latest_value = latest_value


cipi = Person("Cipi", 1, 0)
stefan = Person("Stefan", 2, 0)
