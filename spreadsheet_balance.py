import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
sheet = client.open('Balance').sheet1

# def change_order(first_row, last_row):
# for i in range(first_row, last_row + 1):
# values_last_row = sheet.row_values(last_row)
# sheet.insert_row(values_last_row, i)
# sheet.delete_row(last_row + 1)


class Balance:
    import gspread

    def __init__(self, name, column_index):
        self.name = name
        self.column_index = column_index
        if(sheet.cell(2, column_index).value):
            self.latest_value = int(sheet.cell(2, column_index).value)
        else:
            self.latest_value = 0
        if (name not in sheet.row_values(1)
                and sheet.cell(1, column_index).value is ""):
            sheet.update_cell(1, column_index, name)
        else:
            print(
                "This column is already occupied or the name is already used")

    def insert_cell(self, value):
        for i in range(len(sheet.col_values(self.column_index)), 1, -1):
            current_cell = sheet.cell(i, self.column_index).value
            sheet.update_cell(i + 1, self.column_index, current_cell)
        sheet.update_cell(2, self.column_index, value)

    def change_balance(self, money_value):
        new_value = self.latest_value + money_value
        self.insert_cell(new_value)


cipi = Balance("Cipi", 1)
stefan = Balance("Stefan", 2)
alex = Balance("Alex", 3)

alex.change_balance(50)
