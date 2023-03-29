import imaplib
import email
import os
import openai
import smtplib
import random
from email.mime.text import MIMEText


# Change your API KEY here -
OPENAI_API_KEY = "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"

imap_host = 'imap.gmail.com'

# Change your email details here -
imap_user = "partbarse92@gmail.com"
imap_pass = "xdfrjwaxctwqpzyg"

def generate_response(message_text):
    prompt = message_text
    response = openai.Completion.create(
        engine='text-davinci-003', prompt=prompt, max_tokens=256, n=1, stop=None, temperature=0.7
    )
    return response.choices[0].text.strip()


def check_mail(num):
    import time as time1
    flag = False
    print("Waiting...")
    openai.api_key = OPENAI_API_KEY
    if emails[0]:
        latest_email = emails[0].split()[-min(num, len(emails)):]
        for j in latest_email:
            body = ""
            res, msg = imap.fetch(j, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    sender_email = msg['From']
                    sender_email = sender_email.split('<')
                    sender_email = sender_email[1].replace(">", "")
                    print(sender_email)
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdispo = str(part.get('Content-Disposition'))

                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                        body = part.get_payload(decode=True).decode()
                        print(body)
                        flag = True
                    else:
                        pass
            if body != "":
                print("Done")
            if flag:
                resp = generate_response(str(body.strip()))
                print(str(resp))
                smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login("partbarse92@gmail.com", "xdfrjwaxctwqpzyg")
                message = MIMEText(resp)
                message["Subject"] = str("Support Request Resolution: Ticket " + str(random.randint(1001, 4200)))
                message["To"] = sender_email
                smtp_server.sendmail(sender_email, sender_email, message.as_string())
                smtp_server.quit()
                flag = False
    else:
        print("No new emails found")

imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)

try:
    imap.select("inbox")
    status, emails = imap.search(None, 'UNSEEN')
    check_mail(1)
except Exception as e:
    print("Error - ", e)

imap.logout()
