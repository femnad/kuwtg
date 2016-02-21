import requests

def get_notification_body(url):
    response = requests.get(url)
    notification = response.json()
    body = notification['body']
    if '_links' in notification:
        links = notification['_links']
    else:
        links = None
    return body, links

def get_comments(url):
    response = requests.get(url)
    raw_comments = response.json()
    comments = [{"user": comment['user']['login'],
                 "comment": comment['body']} for comment in raw_comments]
    return comments
