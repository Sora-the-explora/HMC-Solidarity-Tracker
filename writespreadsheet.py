import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = 'https://www.googleapis.com/auth/drive'
sheet_id = "1E2_oY3esh-Z7xggBtR7Z0ZHk1oPT9WM8wkBzYZ1QClw"

def write_spreadsheet(new_payments):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        raise Exception("Logging in failed. ")

    service = build('sheets', 'v4', credentials=creds)
    incoming_values = [[*i[1:]] for i in new_payments if i[0] == "incoming"]
    outgoing_values = [[*i[1:]] for i in new_payments if i[0] == "outgoing"]
    incoming_body = {'values': incoming_values}
    outgoing_body = {'values': outgoing_values}
    incoming_result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range="Incoming Funds", body=incoming_body, valueInputOption="USER_ENTERED").execute()
    outgoing_result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range="Outgoing Funds", body=outgoing_body, valueInputOption="USER_ENTERED").execute()


if __name__ == "__main__":
    write_spreadsheet(1)
