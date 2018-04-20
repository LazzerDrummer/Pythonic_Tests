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


def get_names():
    pp.pprint(sheet.row_values(1))


def get_balances():
    # pp.pprint(sheet.range(2, 2, 2, sheet.col_count))
    for j in range(2, sheet.col_count + 1):
        for i in range(1, 3):
            print(sheet.cell(i, j).value, end=" ")
        print()


class Balance:

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
            sheet.add_cols(1)
            self.column_index = sheet.col_count + 1
            sheet.update_cell(1, self.column_index, name)
            self.latest_value = 0
            self.len_this_col = 0

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
        if self.latest_value != 0:
            self.insert_cell(0)

    def delete_latest_cell(self):
        if self.len_this_col != 1:
            for i in range(3, self.len_this_col + 1):
                current_cell = sheet.cell(i, self.column_index).value
                sheet.update_cell(i - 1, self.column_index, current_cell)
            sheet.update_cell(self.len_this_col, self.column_index, "")
            self.update_lastest_value()


if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv) > 5:
        print('Type "python spreadsheet_balance help" to understand what you '
              + 'can do with this program')
        print('usage: python spreadsheet_balance.py (function) '
              + '(argument1) ' + '(argument2)')
        sys.exit(1)
    elif sys.argv[1] == 'change-balance':
        if len(sys.argv) != 4:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            person.change_balance(int(sys.argv[3]))
    elif sys.argv[1] == 'delete-latest-cell':
        if len(sys.argv) != 3:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            person.delete_latest_cell()
    elif sys.argv[1] == 'add-person':
        if len(sys.argv) != 3:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            if person.new_person:
                print('[insert function help here]')
                sys.exit(1)
    elif sys.argv[1] == 'nullify':
        if len(sys.argv) != 3:
            print('[insert function help here]')
            sys.exit(1)
        else:
            person = Balance(sys.argv[2])
            person.nullify()
    elif sys.argv[1] == 'get-names':
        if len(sys.argv) != 2:
            print('[insert function help here]')
            sys.exit(1)
        else:
            get_names()
    elif sys.argv[1] == 'get-balances':
        if len(sys.argv) != 2:
            print('[insert function help here]')
            sys.exit(1)
        else:
            get_balances()
