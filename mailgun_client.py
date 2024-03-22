from dotenv import load_dotenv
load_dotenv()
from typing import Optional
import os
import requests

class MailGun():
    url:Optional[str] =None
    auth:Optional[str]=None 
    route_url:Optional[str]=None

    def __init__(self):
        self.url: str = os.environ.get("MAILGUN_URL")
        self.route_url: str = os.environ.get("MAILGUN_ROUTE_URL")
        self.auth = ("api", os.environ.get("MAILGUN_SECRET"))

    # [TO], [CC], [SUBJECT], [EMAIL HEADING], [EMAIL CONTENT]
    def send_email_message(self, to, cc,subject,heading = None, content = None):
        response =  requests.post(
            url = f'{self.url}/messages',
            auth=self.auth,
            data={"from": "Steve <steve@trygepeto.com>" ,
                "to": to,
                "cc":cc,
                "subject": subject,
                "html": "Hi there, I'm now trying this from the main domain"}
		)
        return response
    
#send tp uzair@hellogepeto.com 
mg = MailGun()
test = mg.send_email_message("uzair@hellogepeto.com", "", "Test Email")
print(test)



        

