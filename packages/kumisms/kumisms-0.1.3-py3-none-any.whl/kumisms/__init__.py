import urllib.request
import urllib.parse
import json

URL = "https://kumisms.com/api/v1/"

class InvalidCredentials(Exception):
    pass

class SendFailed(Exception):
    pass

class RateUnavailable(Exception):
    pass

class KumiSMS:
    def __init__(self, key, endpoint=URL):
        self.key = key
        self.endpoint = endpoint
        self.check()

    def send(self, recipient, text):
        endpoint = urllib.parse.urljoin(self.endpoint, "send/")
        content = self._request(endpoint, {"recipient": recipient, "text": text})
        if content["status"] == "error":
            raise SendFailed(content["error_message"])
        return True

    def balance(self):
        endpoint = urllib.parse.urljoin(self.endpoint, "balance/")
        return self._request(endpoint)["balance"]

    def rate(self, recipient, text=""):
        endpoint = urllib.parse.urljoin(self.endpoint, "rate/")
        content = self._request(endpoint, {"recipient": recipient, "text": text})
        if content["status"] == "error":
            raise RateUnavailable(content["error_message"])
        return content["rate"]

    def check(self):
        return bool(self.balance())

    def _request(self, url, data={}):
        data.update({"key": self.key})
        body = json.dumps(data).encode()
        request = urllib.request.urlopen(url, body)
        content = json.loads(request.read())
        if content["status"] == "error":
            if content["error_message"] == "Incorrect API key":
                raise InvalidCredentials(content["error_message"])
        return content
