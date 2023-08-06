from typing import List

from requests import Session

from ._baseapi import BaseAPI
from ._pagination import Pagination
from .studentdb import StudentDBAPI
from .users import UsersAPI


class Client:
    def __init__(self, token: str, base_url='https://api.scoredb.tech'):
        if not token:
            raise ValueError('An API token is required.')
        self.session = Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'User-Agent': 'sdk/python'
        })
        self.base_url = base_url
        while self.base_url[-1] == '/':
            self.base_url = self.base_url[:-1]

        # Register APIs
        self.users = UsersAPI(self.session, self.base_url)
        self.studentdb = StudentDBAPI(self.session, self.base_url)

    def apis(self) -> List[BaseAPI]:
        return [self.users, self.studentdb]
