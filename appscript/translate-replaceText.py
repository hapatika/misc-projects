from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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

'''
function replaceText() {
  let tr = '{ "我们的基金公司" : "Our Fundhouses", "我们的业务合作伙伴" : "Our Business Partners"}';
  var trn = JSON.parse(tr);
  // var slides = SlidesApp.getActivePresentation().getSlides();
  var activeSlide = SlidesApp.getActivePresentation().getActiveSlide();
  // ID = editor-g22ec9073485_0_579
  // fix the ID thing man
  var content = fundHouse.getPageElementById('g22ec9073485_0_579').asShape();
  var text = content.getText();
  try{
    for(var i in trn){
      console.log("%s", i);
      text.replaceAllText(i, trn[i]);
      // if(text.search(i)!=-1){
        // text.setText(trn[i]);
        // break;
      // }
    }
    console.log("Yurr");
  } catch(err) {
    console.log('FAILURE!');
  }
}'''