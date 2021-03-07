import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # service = build('gmail', 'v1', credentials=creds)
    #
    # # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])
    #
    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])
    #
    # query="from:venmo@venmo.com"
    # response = service.users().messages().list(userId="me", q=query).execute()
    # messages = []
    # if 'messages' in response:
    #     messages.extend(response['messages'])
    # while 'nextPageToken' in response:
    #     page_token = response['nextPageToken']
    #     response = service.users().messages().list(userId="me", q=query, pageToken=page_token).execute()
    #     messages.extend(response['messages'])
    # for message in [messages[5]]:
    #     email = service.users().messages().get(userId= 'me', id= str(message["id"])).execute()
    #     snippet= email['snippet']
    #     print(snippet)
    #     payerName= str.lower(snippet[:snippet.index("paid You")].strip())
    #     dollarPos= snippet.index("$")
    #     decimalPos= snippet.index(".", dollarPos)
    #     payerAmt= snippet[dollarPos+1:decimalPos+3].strip()
    #     print(payerName)
    #     print(payerAmt)

if __name__ == '__main__':
    main()
