class ResponseNotOkException(Exception):

    def __init__(self, response_text):
        self._response_text = response_text

    def __str__(self):
        return self._response_text
