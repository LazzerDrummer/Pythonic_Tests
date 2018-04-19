import sys
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


def get_names(self):
    pp.pprint(sheet.row_values(1))


class Balance:
    # import gspread
    # new_person = False

    def __init__(self, name):
        self.name = name
        self.new_person = False
        # self.column_index = column_index
        iteration = 0
        for value in sheet.row_values(1):
            iteration += 1
            if name == value:
                self.column_index = iteration
                if sheet.cell(2, self.column_index).value is not "":
                    self.latest_value = int(
                        sheet.cell(2, self.column_index).value)
                else:
                    self.latest_value = 0
                self.len_this_col = len(sheet.col_values(self.column_index))
                self.new_person = True
        if not self.new_person:
            print('yay1')
            sheet.add_cols(1)
            self.column_index = sheet.col_count + 1
            sheet.update_cell(1, self.column_index, name)
            self.latest_value = 0
            self.len_this_col = 0
        # if name not in sheet.row_values(1):
        #     if(sheet.col_count < column_index):
        #         sheet.add_cols(1)
        #         sheet.update_cell(1, column_index, name)
        #         self.latest_value = 0
        #         self.len_this_col = 0
        #     else:
        #         print("This column is already in use")
        # else:
        #     print("This name is already used")
        #     self.column_index = col
        #     self.latest_value = int(sheet.cell(2, column_index).value)
        #     self.len_this_col = len(sheet.col_values(self.column_index))

    def update_lastest_value(self):
        if sheet.cell(2, self.column_index).value is not "":
            self.latest_value = int(
                sheet.cell(2, self.column_index).value)
        else:
            self.latest_value = 0

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
        if self.len_this_col != 1:
            for i in range(3, self.len_this_col + 1):
                current_cell = sheet.cell(i, self.column_index).value
                sheet.update_cell(i - 1, self.column_index, current_cell)
            sheet.update_cell(self.len_this_col, self.column_index, "")
            self.update_lastest_value()


if __name__ == '__main__':
    if len(sys.argv) == 2 or len(sys.argv) > 5:
        print('Type "python spreadsheet_balance help" to understand what you '
              + 'can do with this program')
        print('usage: python spreadsheet_balance.py (function) '
              + '(argument1) ' + '(argument2)')
        sys.exit(1)
    elif sys.argv[1] == 'change_balance':
        if len(sys.argv) != 4:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            person.change_balance(int(sys.argv[3]))
    elif sys.argv[1] == 'delete_latest_cell':
        if len(sys.argv) != 3:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            person.delete_latest_cell()
    elif sys.argv[1] == 'add_person':
        if len(sys.argv) != 3:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            if person.new_person:
                print('[insert function help here]')
                sys.exit(1)
