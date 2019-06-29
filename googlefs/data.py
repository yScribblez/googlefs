from __future__ import print_function
import pprint
import pickle
import os.path
import constants
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
def get_authenticated_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(constants.TOKEN_FILE):
        with open(constants.TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                constants.CREDENTIALS_FILE, constants.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(constants.TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build(constants.SERVICE, constants.VERSION, credentials=creds)
    return service

def get_file_data(service, **kwargs):
    # Call the Drive v3 API
    results = service.files().list(**kwargs).execute()
    return results

def get_file_list(service):
    results = get_file_data(service, fields='files(name)', orderBy='modifiedByMeTime desc').get('files', [])
    files = [d['name'] for d in results]
    return files

if __name__ == '__main__':
    service = get_authenticated_service()
    results = get_file_data(service, orderBy='modifiedByMeTime desc', pageSize=5)
    pp = pprint.PrettyPrinter(indent=2)
    print(type(results['files']))
    pp.pprint(results)
    files = get_file_list(service)
    print(files)
