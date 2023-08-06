import os
import json

from .person import Person
from .verbose import VERBOSE


class Service():
    def __init__(self, conn, username, service_name, data):
        self.__dict__['username'] = username
        self.__dict__['service_name'] = service_name
        self.__dict__['conn'] = conn
        self.__dict__['data'] = data
        self.__dict__['updated_attrs'] = {}

    def revoke(self):
        pass

    def save(self):
        if not self.updated_attrs:
            return

        endpoint = f'/usermgr/user/{self.username}/service/{self.service_name}'
        resp = self.conn._put_request(endpoint, self.updated_attrs)
        if resp.ok:
            if VERBOSE:
                print(f"Attributes for user {self.username} and service {self.service_name} updated.")
        elif resp.status_code == 401:
            raise ValueError('You are not allowed to do this operation')
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])


class Mailbox(Service):

    def __dir__(self):
        return ['sn', 'givenName', 'displayName', 'description', 'mail', 'isHidden', 'noMailReceive', 'quota', 'homeDrive', 'homeDirectory', 'profilePath', 'unixHomeDirectory', 'loginShell', 'primaryGroup', 'unifiedMessagingTask', 'telephoneNumber', 'forward_address', 'proxyAddresses'
        ]

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        self.__dict__['updated_attrs'][name] = value


    def __getattr__(self, name):
        return self.__dict__[name]
