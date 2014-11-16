# !/usr/bin/pyhton
# github.py used for contacting github.

import json
import sys

from urllib.request import urlopen
from urllib.parse import urlencode

from exceptions import ValidationException
from configs import ISSUES_URL, AUTH_TOKEN

DEFAULT_TITLE = '<no title>'


class GithubSAO:

    def __init__(self):
        pass

    def create_issue(self, title=None, body=None, assignee=None, labels=None):
        title = title or DEFAULT_TITLE
        labels = labels or []
        data = {"title": title,
                "body": body,
                "assignee": assignee,
                "labels": labels
                }
        encoded_data = json.dumps(data).encode(encoding='utf_8')
        params = urlencode({'access_token': AUTH_TOKEN})
        issues_url_with_auth_token = ISSUES_URL + '?' + params
        response = urlopen(issues_url_with_auth_token, data=encoded_data)
        if(response.status == 201):
            print('Created issue..{}'.format(data))
        return response


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test()
    else:
        response = GithubSAO().create_issue('TestModTitle', 'Test', None)
        print(response.status)


def test():
    pass

if __name__ == "__main__":
    main()
