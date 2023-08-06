from requests import Session


class BaseAPI:

    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url

    def __repr__(self):
        return f'<ScoreDB {type(self).__name__} Endpoint object>'

    def request(self, method: str, uri: str, **kwargs):
        if uri[0] != '/':
            uri = '/' + uri
        url = self.base_url + uri
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
