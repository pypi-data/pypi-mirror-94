from ._baseapi import BaseAPI
from ..models import User


class UsersAPI(BaseAPI):

    def get_current_user(self):
        result = self.request('GET', '/user')
        return User(**result)
