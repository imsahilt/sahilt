# !/usr/bin/python
# bot.py is main class which runs infinitely.
import sys
import logging
from time import sleep

from configs import DEFAULT_FETCH_INTERVAL, EMAIL_ACCOUNT, PASS, EMAIL_FOLDER, LOG_FORMAT, LOG_FILE
from github import GithubSAO
from exceptions import RetryableException, NonRetryableException
from emails import EmailSAO

logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


class Bot():

    def __init__(self, github_sao, email_sao,
                 fetch_interval=DEFAULT_FETCH_INTERVAL):
        self._github_sao = github_sao
        self._email_sao = email_sao
        self._fetch_interval = fetch_interval

    def _handle_exception(self, e):
        if isinstance(e, RetryableException):
            logger.debug("Got an RetryableException will try later...error:{}".format(e))
        elif isinstance(e, NonRetryableException):
            logger.error("Got an NonRetryableException exiting...{}".format(e))
            sys.exit(1)  # Alarm
        else:
            logger.error("I don't know what happened, exiting...{}".format(e))
            sys.exit(1)  # Alarm

    def do_action(self):
        while True:
            try:
                email_list = self._email_sao.get_emails()
                logger.info("Got {} messages to process..".format(len(email_list)))
                for email in email_list:
                    try:  # Process rest of the list even if one message is faulty.
                        title = email.get_email_subject()
                        body = email.get_email_body()
                        self._github_sao.create_issue(title, body)
                        self._email_sao.mark_message_seen(email.get_header())  # mark message seen only after processing is complete
                    except Exception as e:
                        self._handle_exception(e)
            except Exception as e:
                self._handle_exception(e)

            logger.info("sleeping for {} seconds..".format(self._fetch_interval))
            sleep(self._fetch_interval)


def main():
    bot = Bot(GithubSAO(), EmailSAO(EMAIL_ACCOUNT, PASS, EMAIL_FOLDER))
    bot.do_action()

if __name__ == "__main__":
    main()
