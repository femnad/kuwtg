import requests

def get_notification_body(url):
    response = requests.get(url)
    notification = response.json()
    return notification['body']
