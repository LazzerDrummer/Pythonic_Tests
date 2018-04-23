import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from inspect import signature
import pprint


scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
sheet = client.open('Debt').sheet1

rows = sheet.row_count
cols = sheet.col_count

values_last_row = sheet.row_values(rows)


def get_names():
    pp.pprint(sheet.row_values(1))


def get_debts():
    for j in range(2, cols + 1):
        for i in range(1, 3):
            print(sheet.cell(i, j).value, end=" ")
        print()


def check_last_row_null():
    for value in values_last_row:
        if value is not "":
            return False
    return True


class Debt:

    def __init__(self, name):
        self.name = name
        self.new_person = False
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
            self.column_index = cols + 1
            sheet.update_cell(1, self.column_index, name)
            self.latest_value = 0
            self.len_this_col = 0

    def update_latest_value(self):
        if sheet.cell(2, self.column_index).value is not "":
            self.latest_value = int(
                sheet.cell(2, self.column_index).value)
        else:
            self.latest_value = 0

    def insert_cell(self, value):
        if sheet.cell(rows, self.column_index).value is not "":
            sheet.add_rows(1)
        for i in range(self.len_this_col, 1, -1):
            current_cell = sheet.cell(i, self.column_index).value
            sheet.update_cell(i + 1, self.column_index, current_cell)
        sheet.update_cell(2, self.column_index, value)

    def change_debt(self, money_value):
        try:
            money_value = int(money_value)
        except ValueError:
            print()
            print("This function takes in an int value, a whole number "
                  + "that can be either negative or positive.")
        else:
            new_value = self.latest_value + money_value
            self.insert_cell(new_value)
            self.update_latest_value()

    def nullify(self):
        if self.latest_value != 0:
            self.insert_cell(0)

    def delete_latest_cell(self):
        if self.len_this_col != 1:
            for i in range(3, self.len_this_col + 1):
                current_cell = sheet.cell(i, self.column_index).value
                sheet.update_cell(i - 1, self.column_index, current_cell)
            sheet.update_cell(self.len_this_col, self.column_index, "")
            self.update_latest_value()
            if check_last_row_null():
                sheet.delete_row(rows)

    def get_debt(self):
        print(self.latest_value)


if __name__ == '__main__':
    if len(sys.argv) == 1 or len(sys.argv) > 5:
        print('Type "python spreadsheet_debt help" to understand what you '
              + 'can do with this program')
        sys.exit(1)
    else:
        if hasattr(Debt, sys.argv[1]):
            if callable(getattr(Debt, sys.argv[1])):
                if(len(sys.argv) >= 3):
                    person = Debt(sys.argv[2])
                else:
                    print("This function requires a Debt object")
                    print("more help here")
                    sys.exit(1)
                method = getattr(person, sys.argv[1])
                sig = signature(method)
                params = sig.parameters
                if(len(params) == len(sys.argv) - 3):
                    if len(params) == 0:
                        method()
                    elif len(params) == 1:
                        method(sys.argv[3])
                else:
                    print("insert help here")
            else:
                print("The Debt class does not have this function.")
                sys.exit(1)
        else:
            if len(sys.argv) == 2:
                if sys.argv[1] == 'get_names':
                    get_names()
                elif sys.argv[1] == 'get_debts':
                    get_debts()
                else:
                    print("This python program not have this function.")
            else:
                print("insert help here")
