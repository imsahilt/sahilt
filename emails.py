# !/usr/bin/python
# email.py is used to connect to imap server and extract emails
import sys
import imaplib
import email.header
import logging

from exceptions import InvalidEmailFolderException, MessageNotFoundException, InvalidCredentials, InvalidSearchCriteria
from configs import IMAP_URL, EMAIL_FOLDER, DEFAUT_EMAIL_LIMIT, LOG_FORMAT, LOG_FILE

logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_BODY = '<no body>'
MESSAGE_PARTS = '(RFC822)'
SUCCESS = 'OK'
FOLDER_SEARCH_CRITERIA = '(UNSEEN)'
FLAGS_COMMAND = '+FLAGS'
SEEN_FLAG = '\\Seen'


class Email:
    """
        This class contains structure of get_email response and
        parser methods to extract parts of email_message.
    """
    def __init__(self, header, message):
        self._header = header
        self._email_message = message

    def get_header(self):
        """
            gets header of email.
        """
        return self._header

    def get_email_message(self):
        """
            gets the email message.
        """
        return self._email_message

    def get_email_subject(self):
        """
            Returns subject of email after decoding it from email header.
        """
        subject = email.header.decode_header(self._email_message['Subject'])[0][0]
        return subject

    def get_email_body(self):
        """
            Extracts email body from email message
        """
        body = DEFAULT_BODY
        content_type = 'Content-Type'
        if 'text/plain' in str(self._email_message.get_payload()[0][content_type]):
            body = str(self._email_message.get_payload()[0])  # get plain text.
        elif 'multipart/alternative' in str(self._email_message.get_payload()[0][content_type]):
            body = str(self._email_message.get_payload()[0].get_payload()[0])
        return body


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
        self._imap = imaplib.IMAP4_SSL(IMAP_URL)
        try:
            self._imap.login(self._uname, self._password)
        except imaplib.IMAP4.error as e:
            logger.error('Damn!! login failed with error:{}'.format(e))
            raise InvalidCredentials('Damn!! login failed with error:{}'.format(e))

    def _search_emails(self):
        """
            Search Emails based on search criteria and raise RetryableException
            for poller
        """
        resp = self._imap.search(None, FOLDER_SEARCH_CRITERIA)
        if resp[0] != SUCCESS:
            logger.error('Invalid search criteria {}'.format(FOLDER_SEARCH_CRITERIA))
            raise InvalidSearchCriteria('Invalid search criteria {}'.format(FOLDER_SEARCH_CRITERIA))
        return resp[1]

    def _get_email_list(self, limit):
        """
            Parse and build List of email messages.
        """
        resp = self._search_emails()
        if not resp[0]:
            logger.debug('No emails with given search criteria:{}'.format(FOLDER_SEARCH_CRITERIA))
        emails_response = []
        counter = 1
        for num in resp[0].split():  # Iterate through list of emails
            message = self._imap.fetch(num, MESSAGE_PARTS)  # Fetch email body
            if message[0] != SUCCESS:
                logger.warn("ERROR getting message number:{}".format(num))
                raise MessageNotFoundException("ERROR getting message number:{}".format(num))
            parsed_message = email.message_from_bytes(message[1][0][1])
            emails_response.append(Email(num, parsed_message))  # build email response
            if counter > limit:  # as gmail does not provide limited fetching
                break
            counter = counter + 1
        return emails_response

    def get_emails(self, limit=DEFAUT_EMAIL_LIMIT):
        """
            Fetch emails from specified folder and return a list of
            Email messages.
        """
        self._login()
        # Read-only true so that we can handle the case of process dying in during processing of email message.
        resp = self._imap.select(self._email_folder, readonly=True)
        if resp[0] == SUCCESS:
            email_message_list = self._get_email_list(limit)
            self._imap.close()
        else:
            logger.error('Email folder:{} can not be selected'.format(self._email_folder))
            raise InvalidEmailFolderException('Email folder can not be selected')
        self._logout()
        return email_message_list

    def mark_message_seen(self, unseen_message_header):
        """
            Marks message unseen for unseen_message_header.
        """
        self._login()  # TODO: find a better way
        resp = self._imap.select(self._email_folder)
        if resp[0] == SUCCESS:
            self._imap.store(unseen_message_header, FLAGS_COMMAND, SEEN_FLAG)
            logger.info('Successfully marked {} :header seen'.format(unseen_message_header))
            self._imap.close()
        else:
            logger.error('Email folder:{} can not be selected while marking message read'.format(self._email_folder))
            raise InvalidEmailFolderException('Email folder can not be selected')
        self._logout()

    def _logout(self):
        """
            logout of email account.
        """
        self._imap.logout()


def main():
    emailSao = EmailSAO('imsahilt@gmail.com', 'T3st1234', EMAIL_FOLDER)  # TODO: remove
    email_message_list = emailSao.get_emails()
    for email in email_message_list:
        print(email.get_email_subject())
        print(email.get_email_body())
        emailSao.mark_message_seen(email.get_header())

if __name__ == "__main__":
    main()
