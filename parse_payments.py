import pickle
import os.path
import datetime
import base64
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class EmailParseError(Exception):
 def __init__(self, arg):
  self.strerror = arg
  self.args = {arg}

def parse_snippet(snippet, body):
    if "You paid" in snippet:
        dollarPos= snippet.index("$")
        decimalPos= snippet.index(".", dollarPos)
        payerAmt= snippet[dollarPos+1:decimalPos+3].strip()
        soup = BeautifulSoup(body, "lxml")
        payerName = soup.find_all('a')[2].text
        payerName = payerName.replace('\\r', '')
        payerName = payerName.replace('\\n', '').strip()
        return ("outgoing", payerName, payerAmt)
    elif "paid You" in snippet:
        payerName= str.lower(snippet[:snippet.index("paid You")].strip())
        dollarPos= snippet.index("$")
        decimalPos= snippet.index(".", dollarPos)
        payerAmt= snippet[dollarPos+1:decimalPos+3].strip()
        return ("incoming", payerName, payerAmt)
    raise EmailParseError("Not a payment notification.")


def parse_payments(date_after):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Logging in failed. ")

    service = build('gmail', 'v1', credentials=creds)
    stringDate= str(date_after.year)+"/"+str(date_after.month)+"/"+str(date_after.day)

    query=f"from:venmo@venmo.com after:{stringDate}"
    response = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId="me", q=query, pageToken=page_token).execute()
        messages.extend(response['messages'])
    payments = []
    for message in messages:
        try:
            email = service.users().messages().get(userId= 'me', id= str(message["id"])).execute()
            snippet= email['snippet']
            payload = email['payload']
            parts = payload.get('parts')[1]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = str(base64.b64decode(data))
            result = parse_snippet(snippet, decoded_data)
            header = payload['headers']
            for item in header:
                if item['name'] == 'Date':
                    date = item['value']
            payments.append((*result,date))
        except EmailParseError:
            pass
        except Exception:
            pass
    return payments
