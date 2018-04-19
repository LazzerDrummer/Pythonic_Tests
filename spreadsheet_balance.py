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
    # import gspread
    def __init__(self, name, column_index):
        self.name = name
        self.column_index = column_index
        if name not in sheet.row_values(1):
            if(sheet.col_count < column_index):
                sheet.add_cols(1)
                sheet.update_cell(1, column_index, name)
                self.latest_value = 0
                self.len_this_col = 0
            else:
                print("This column is already in use")
        else:
            print("This name is already used")
            self.latest_value = int(sheet.cell(2, column_index).value)
            self.len_this_col = len(sheet.col_values(self.column_index))

    def update_lastest_value(self):
        self.latest_value = int(sheet.cell(2, self.column_index).value)

    def insert_cell(self, value):
        if sheet.cell(sheet.row_count, self.column_index).value is not "":
            sheet.add_rows(1)
        for i in range(self.len_this_col, 1, -1):
            current_cell = sheet.cell(i, self.column_index).value
            sheet.update_cell(i + 1, self.column_index, current_cell)
        sheet.update_cell(2, self.column_index, value)

    def change_balance(self, money_value):
        new_value = self.latest_value + money_value
        self.insert_cell(new_value)
        self.update_lastest_value()

    def nullify(self):
        self.insert_cell(0)

    def delete_latest_cell(self):
        for i in range(3, self.len_this_col + 1):
            current_cell = sheet.cell(i, self.column_index).value
            sheet.update_cell(i - 1, self.column_index, current_cell)
        sheet.update_cell(self.len_this_col, self.column_index, "")
        self.update_lastest_value()


# cipi = Balance("Cipi", 2)
# stefan = Balance("Stefan", 3)
# alex = Balance("Alex", 4)
# paul = Balance("Paul", 5)
