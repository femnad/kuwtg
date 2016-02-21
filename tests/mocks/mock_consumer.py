class MockAPIConsumer(object):

    NUMBER_OF_ITEMS = 50
    NUMBER_OF_COMMENTS = 10

    def get_notifications(self, dummy):
        return [{'id': index,
                 'subject': {'type': 'dummy',
                             'title': "Item {}".format(index),
                             'url': 'http://www.example.com'}}
                 for index in range(self.NUMBER_OF_ITEMS)]

    def get_notification_body(self, dummy):
        body = "Item body"
        links = {'comments':{'href':'http://www.example.com'}}
        return body, links

    def get_comments(self, dummy):
        return [{"comment": "comment {}".format(index), "user": "user {}".format(index)}
                for index in range(self.NUMBER_OF_COMMENTS)]
