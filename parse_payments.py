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

def parse_snippet(snippet):
    if "You paid" in snippet:
        payerName= str.lower(snippet[snippet.index("You paid"):snippet.index("$")].strip())
        dollarPos= snippet.index("$")
        decimalPos= snippet.index(".", dollarPos)
        payerAmt= snippet[dollarPos+1:decimalPos+3].strip()
        return ("outgoing", payerAmt, payerName)
    elif "paid You" in snippet:
        payerName= str.lower(snippet[:snippet.index("paid You")].strip())
        dollarPos= snippet.index("$")
        decimalPos= snippet.index(".", dollarPos)
        payerAmt= snippet[dollarPos+1:decimalPos+3].strip()
        return ("incoming", payerAmt, payerName)
    raise EmailParseError("Not a payment notification.")


def parse_payments():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        raise Exception("Logging in failed. ")

    service = build('gmail', 'v1', credentials=creds)
    today=datetime.datetime.now()
    x =  datetime.date(today.year,today.month, today.day) + timedelta(weeks=-52)
    stringDate= str(x.year)+"/"+str(x.month)+"/"+str(x.day)

    query=f"from:venmo@venmo.com after:{stringDate}"
    response = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId="me", q=query, pageToken=page_token).execute()
        messages.extend(response['messages'])
    for message in [messages[1]]:
        email = service.users().messages().get(userId= 'me', id= str(message["id"])).execute()
        snippet= email['snippet']
        payload = email['payload']
        parts = payload.get('parts')[1]
        data = parts['body']['data']
        data = data.replace("-","+").replace("_","/")
        decoded_data = str(base64.b64decode(data))
        soup = BeautifulSoup(decoded_data , "lxml")
        body = soup.body()
        name = soup.find_all('a')[2].text
        name = name.replace('\\r', '')
        name = name.replace('\\n', '').strip()
        print(name)
        # for item in soup.find_all('a'):
        #     print(item)
        #     print("\n\n\n ARYA")
        # indx = decoded_data.index("You paid")
        # print(decoded_data)
        try:
            result = parse_snippet(snippet)
            print(result)
        except EmailParseError:
            print("hehe no")
            pass


if __name__ == "__main__":
    parse_payments()
