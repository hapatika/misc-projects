# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START apps_script_api_quickstart]
"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/script.projects']

SAMPLE_CODE = '''
function replaceText() {
  let tr = '{ "我们的基金公司" : "Our Fundhouses", "我们的业务合作伙伴" : "Our Business Partners"}';
  var trn = JSON.parse(tr);
  var activeSlide = SlidesApp.getActivePresentation().getActiveSlide();
  // ID = editor-g22ec9073485_0_579
  var content = fundHouse.getPageElementById('g22ec9073485_0_579').asShape();
  var text = content.getText();
  try{
    for(var i in trn){
      console.log("%s", i);
      text.replaceAllText(i, trn[i]);
    }
    console.log("Yurr");
  } catch(err) {
    console.log('FAILURE!');
  }
}
'''.strip()

SAMPLE_MANIFEST = '''
{
  "timeZone": "America/New_York",
  "exceptionLogging": "CLOUD"
}
'''.strip()

# [START slides_simple_text_replace]

def simple_text_replace(presentation_id, shape_id, replacement_text):
    """
    Run simple_text_replace the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        slides_service = build('slides', 'v1', credentials=creds)
        # Remove existing text in the shape, then insert new text.
        requests = []
        requests.append({
            'deleteText': {
                'objectId': shape_id,
                'textRange': {
                    'type': 'ALL'
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': shape_id,
                'insertionIndex': 0,
                'text': replacement_text
            }
        })

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print(f"Replaced text in shape with ID: {shape_id}")
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Text is not merged")
        return error


if __name__ == '__main__':
    # Put the presentation_id, shape_id and replacement_text
    simple_text_replace('10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4',
                        'MyTextBox_6',
                        'GWSpace_now')


def main():
    """Calls the Apps Script API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('script', 'v1', credentials=creds)

        # Call the Apps Script API
        # Create a new project
        request = {'title': 'My Script'}
        response = service.projects().create(body=request).execute()

        # Upload two files to the project
        request = {
            'files': [{
                'name': 'hello',
                'type': 'SERVER_JS',
                'source': SAMPLE_CODE
            }, {
                'name': 'appsscript',
                'type': 'JSON',
                'source': SAMPLE_MANIFEST
            }]
        }
        response = service.projects().updateContent(
            body=request,
            scriptId=response['scriptId']).execute()
        print('https://script.google.com/d/' + response['scriptId'] + '/edit')
    except errors.HttpError as error:
        # The API encountered a problem.
        print(error.content)


if __name__ == '__main__':
    main()
# [END apps_script_api_quickstart]
