# !/usr/bin/python
# email.py is used to connect to imap server and extract emails
import sys
import imaplib
import email.header

from exceptions import InvalidEmailFolderException, MessageNotFoundException
from configs import IMAP_URL, EMAIL_FOLDER, FOLDER_SEARCH_CRITERIA, DEFAUT_EMAIL_LIMIT

DEFAULT_BODY = '<no body>'


class EmailSAO:
    def __init__(self, uname, password, email_folder):
        self._imap = None
        self._uname = uname
        self._password = password
        self._email_folder = email_folder

    def _login(self):
        """
            Login to email account.
        """
        try:
            data = self._imap.login(self._uname, self._password)
        except imaplib.IMAP4.error as e:
            print('Damn!! login failed with error:{}'.format(e))
            sys.exit(1)  # TODO:
        return data

    def _search_emails(self):
        """
            Search Emails based on search criteria and raise RetryableException
            for poller
        """
        resp = self._imap.search(None, FOLDER_SEARCH_CRITERIA)
        if resp[0] != 'OK':
            raise MessageNotFoundException('No emails with given search criteria:{}'.format(FOLDER_SEARCH_CRITERIA))
        return resp[1]

    def _get_email_list(self, limit):
        """
            Parse and build List of email messages.
        """
        resp = self._search_emails()

        email_message_list = []
        counter = 1
        for num in resp[0].split():  # Iterate through list of emails
            message = self._imap.fetch(num, '(RFC822)')  # Fetch email body
            if message[0] != 'OK':
                raise MessageNotFoundException("ERROR getting message number:{}".format(num))
            parsed_message = email.message_from_bytes(message[1][0][1])
            email_message_list.append(parsed_message)
            if counter > limit:
                break
            counter = counter + 1

        return email_message_list

    def get_emails(self, limit=DEFAUT_EMAIL_LIMIT):
        """
            Fetch emails from specified folder and return a list of email messages.
        """
        self._imap = imaplib.IMAP4_SSL(IMAP_URL)
        self._login()
        resp = self._imap.select(self._email_folder)
        if resp[0] == 'OK':
            email_message_list = self._get_email_list(limit)
            self._imap.close()
        else:
            raise InvalidEmailFolderException('Email folder can not be selected')
        self._imap.logout()  # TODO:
        return email_message_list

    def get_email_subject(self, email_message):
        """
            Returns subject of email after decoding it from email header.
        """
        subject = email.header.decode_header(email_message['Subject'])[0][0]
        return subject

    def get_email_body(self, email_message):
        """
            Parses email body from email message
        """
        body = DEFAULT_BODY
        if 'text/plain' in str(email_message.get_payload()[0]['Content-Type']):
            body = str(email_message.get_payload()[0])
        elif 'multipart/alternative' in str(email_message.get_payload()[0]['Content-Type']):
            body = str(email_message.get_payload()[0].get_payload()[0])
        return body


def main():
    emailSao = EmailSAO('imsahilt@gmail.com', 'T3st1234', EMAIL_FOLDER)
    email_message_list = emailSao.get_emails()
    print(email_message_list)
    for email in email_message_list:
        print(emailSao.get_email_subject(email))
        print(emailSao.get_email_body(email))

if __name__ == "__main__":
    main()
