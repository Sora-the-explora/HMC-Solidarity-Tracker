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

    start = [['name', 'amount', 'date']]
    service = build('sheets', 'v4', credentials=creds)
    incoming_values = [[*i[1:]] for i in new_payments if i[0] == "incoming"]
    outgoing_values = [[*i[1:]] for i in new_payments if i[0] == "outgoing"]
    gfm_body = {'values' : [[raisedGFM]]}
    incoming_sheet = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="Incoming Funds").execute().get('values', [])
    all_incoming = incoming_sheet[1:]+incoming_values
    incoming_formatted = []
    for i in all_incoming:
        try:
            incoming_formatted.append((i[0], float(i[1]), i[2]))
        except:
            pass
    shorter_incoming = list(set(incoming_formatted))

    incoming_body = {'values' : start+shorter_incoming}

    outgoing_sheet = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="Outgoing Funds").execute().get('values', [])
    all_outgoing = outgoing_sheet[1:]+outgoing_values
    outgoing_formatted = [(i[0], float(i[1]), i[2]) for i in all_outgoing]
    shorter_outgoing = list(set(outgoing_formatted))

    outgoing_body = {'values' : start+shorter_outgoing}


    service.spreadsheets().values().clear(spreadsheetId=sheet_id, range='Incoming Funds').execute()
    service.spreadsheets().values().clear(spreadsheetId=sheet_id, range='Outgoing Funds').execute()
    incoming_result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range="Incoming Funds", body=incoming_body, valueInputOption="USER_ENTERED").execute()
    outgoing_result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range="Outgoing Funds", body=outgoing_body, valueInputOption="USER_ENTERED").execute()
    GFM = service.spreadsheets().values().update(spreadsheetId=sheet_id, range="GoFundMe!A2", body=gfm_body,  valueInputOption="USER_ENTERED").execute()
