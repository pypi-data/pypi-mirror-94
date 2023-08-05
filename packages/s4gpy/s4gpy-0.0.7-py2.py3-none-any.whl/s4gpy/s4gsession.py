from urllib.parse import urljoin

from requests import Session


class S4GSession(Session):
    """Wraps a session to provide API baseline."""
    def __init__(self, prefix_url, access_token=None):
        """initialize baseline for API"""
        self.prefix_url = prefix_url
        self.access_token = access_token
        super(S4GSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        if self.access_token is not None:
            if 'headers' in kwargs:
                headers = kwargs["headers"]
            else:
                headers = {}
                kwargs["headers"] = headers
            headers.update(
                {'Authorization':
                 f'Bearer {self.access_token}'})
        return super(S4GSession, self).request(method,
                                               url,
                                               *args,
                                               **kwargs)
