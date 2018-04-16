import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'client_secret.json', scope)
client = gspread.authorize(creds)

pp = pprint.PrettyPrinter()
sheet = client.open('Balance').sheet1
result = sheet.get_all_values()

pp.pprint(result)
