import os
import json

from .verbose import VERBOSE
from .utils import check_password, gen_password


class Person():
    def __init__(self, conn, data=None):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

    def new_user(self, username, password=None, description=None):
        if password is None:
            password = gen_password()
        elif not check_password(password):
            raise ValueError('the initial password must contain at least Lowercase, uppercase characters and a digit')
        if description is None:
            description = username
        endpoint = '/usermgr/person/{}'.format(self.npid)
        body = {
            "username": username,
            "init_passwd": password,
            "memo": description,
        }
        resp = self.conn._post_request(endpoint, body)
        if resp.ok:
            user = self.conn.get_user(username)
            user.init_password = password
            if VERBOSE:
                print("new user {} was successfully created".format(username))
            return user
        elif resp.status_code == 401:
            raise ValueError('Provided admin-username/password is incorrect or you are not allowed to do this operation')
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])
