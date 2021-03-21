import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from GFMscraper import getGFM

SCOPES = 'https://www.googleapis.com/auth/drive'
sheet_id = "13vWTC-2t2f8dFaugRFTVVbrOzncR1H3nyQjOY7ogswM"

def write_spreadsheet(new_payments):
    raisedGFM = getGFM(17050)
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Logging in failed. ")

    service = build('sheets', 'v4', credentials=creds)
    incoming_values = [[*i[1:]] for i in new_payments if i[0] == "incoming"]
    outgoing_values = [[*i[1:]] for i in new_payments if i[0] == "outgoing"]
    incoming_body = {'values': incoming_values}
    outgoing_body = {'values': outgoing_values}
    gfm_body = {'values' : [[raisedGFM]]}
    incoming_result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range="Incoming Funds", body=incoming_body, valueInputOption="USER_ENTERED").execute()
    outgoing_result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range="Outgoing Funds", body=outgoing_body, valueInputOption="USER_ENTERED").execute()
    GFM = service.spreadsheets().values().update(spreadsheetId=sheet_id, range="GoFundMe!A2", body=gfm_body,  valueInputOption="USER_ENTERED").execute()
