#!/usr/bin/env python3
import json

from kuwtg.obj import GithubNotification, GithubComment
from kuwtg.ui import NotificationDetail

def _get_json_from_file(file_name):
    with open(file_name) as file_descriptor:
        json_content = file_descriptor.read()
        return json.loads(json_content)

if __name__ == "__main__":
    test_item = _get_json_from_file('test-notification.json')
    item = GithubNotification(test_item)
    test_starter = _get_json_from_file('test-issue.json')
    starter = GithubComment(test_starter)
    test_comments = _get_json_from_file('test-comments.json')
    comments = [GithubComment(comment) for comment in test_comments]
    notification_detail = NotificationDetail(item, starter, comments)
    notification_detail.draw()
