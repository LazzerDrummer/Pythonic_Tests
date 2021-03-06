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


class Debt:

    count_people = len(sheet.row_values(1))

    def __init__(self, name):
        self.name = name
        self.new_person = True
        iteration = 0
        latest_empty_cell = 0
        for value in sheet.row_values(1):
            iteration += 1
            if latest_empty_cell == 0 and value is "":
                latest_empty_cell = iteration
                continue
            if name == value:
                self.column_index = iteration
                if sheet.cell(2, self.column_index).value is not "":
                    self.latest_value = int(
                        sheet.cell(2, self.column_index).value)
                else:
                    self.latest_value = 0
                self.len_this_col = len(sheet.col_values(self.column_index))
                self.new_person = False
        if cols > len(sheet.row_values(1)) and latest_empty_cell == 0:
            latest_empty_cell = len(sheet.row_values(1)) + 1
        if self.new_person:
            if latest_empty_cell == 0:
                sheet.add_cols(1)
                self.column_index = cols + 1
            else:
                self.column_index = latest_empty_cell
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
        cell_list = sheet.range(2, self.column_index,
                                self.len_this_col + 1, self.column_index)
        for i in range(self.len_this_col - 2, -1, -1):
            current_cell = cell_list[i].value
            cell_list[i+1].value = int(current_cell)
        sheet.update_cells(cell_list)
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

    @staticmethod
    def check_last_row_null():
        if not sheet.row_values(rows):
            return True
        else:
            return False

    def delete_latest_cell(self):
        if self.len_this_col < 3:
            cell_list = sheet.range(2, self.column_index,
                                    self.len_this_col, self.column_index)
            for i in range(0, self.len_this_col - 2):
                current_cell = cell_list[i+1].value
                cell_list[i].value = int(current_cell)
            sheet.update_cells(cell_list)
            sheet.update_cell(self.len_this_col, self.column_index, "")
            self.update_latest_value()
        else:
            sheet.update_cell(2, self.column_index, 0)
        if self.check_last_row_null():
            rows = sheet.row_count
            sheet.delete_row(rows)

    @staticmethod
    def get_names():
        pp.pprint(sheet.row_values(1))

    @staticmethod
    def get_debts():
        cell_list = sheet.range(1, 1, 2, Debt.count_people)
        for i in range(0, Debt.count_people):
            print(cell_list[i].value, end=" ")
            print(cell_list[i + Debt.count_people].value)

    @staticmethod
    def get_sum_of_debts():
        sum = 0
        for value in sheet.row_values(2):
            sum += int(value)
        print(sum)

    def get_debt(self):
        print(self.latest_value)


if __name__ == '__main__':

    if len(sys.argv) == 1 or len(sys.argv) > 5:
        print('Type "python spreadsheet_debt help" to understand what you '
              + 'can do with this program')
        sys.exit(1)
    else:
        attribute = getattr(Debt, sys.argv[1])
        if hasattr(Debt, sys.argv[1]):
            if callable(getattr(Debt, sys.argv[1])):
                if(len(sys.argv) >= 3):
                    person = Debt(sys.argv[2])
                    method = getattr(person, sys.argv[1])
                    difference = 3
                else:
                    method = attribute
                    difference = 2
                sig = signature(method)
                params = sig.parameters
                if(len(params) == len(sys.argv) - difference):
                    if len(params) == 0:
                        method()
                    elif len(params) == 1:
                        method(sys.argv[3])
                else:
                    print("insert help here")
            else:
                print("The Debt class does not have this function.")
        else:
            print("*The Debt class does not have this atribute.")
