import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


# To get all Sheets data
@property
def sheet1(self):
    """Shortcut property for getting the first worksheet."""
    return self.get_worksheet(0)

scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

cwd = os.getcwd()
creds = ServiceAccountCredentials.from_json_keyfile_name(cwd+'/creds.json', scope)
client = gspread.authorize(creds)
wks = client.open("Test").get_worksheet(0)
wks_tenent = client.open("Test").get_worksheet(1)
wks_expenses = client.open("Test").get_worksheet(2)




# Get a list of all records
# get_data = wks.get_all_records()  


def get_data():
    wks = client.open("Test").get_worksheet(0)
    return  wks.get_all_records()  

def get_tenent_data():
    wks = client.open("Test").get_worksheet(1)
    return  wks.get_all_records()  

def get_expenses_data():
    wks = wks_expenses
    return  wks.get_all_records()  

def insert_data(insertRow):
    data =  wks.append_row(insertRow)
    return 'Insertion Done......'

def insert_tenent_data(insertRow):
    data =  wks_tenent.append_row(insertRow)
    return 'Insertion Done......'

def insert_expenses_data(insertRow):
    data =  wks_expenses.append_row(insertRow)
    return 'Insertion Done......'