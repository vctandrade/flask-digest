from codecs import encode
from functools import wraps
from os import urandom
from time import time

from flask import request, make_response
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized
from werkzeug.http import dump_header

from .challenge import Challenge
from .hasher import digest, hash_all
from .maid import Maid

class Token:
    def __init__(self):
        self.timer = time()
        self.used = set()
        self.ip = request.remote_addr

    def stale(self):
        return time() - self.timer > 1800 or len(self.used) > 128

class Stomach:
    def __init__(self, realm):
        self.maid = Maid()
        self.tokens = dict()
        self.realm = realm
        self.qop = 'auth'

    def access(self, func):
        self.get_key = func
        return func

    def get_key(self, username):
        return None

    def register(self, func):
        @wraps(func)
        def wrapper(username, password, *args, **kargs):
            password = hash_all(username, self.realm, password)
            return func(username, password, *args, **kargs)
        return wrapper

    def protect(self, func):
        @wraps(func)
        def wrapper(*args, **kargs):
            self.authenticate()
            response = func(*args, **kargs)
            return self.add_headers(response)
        return wrapper

    def authenticate(self):
        auth = request.authorization
        if auth is None:
            raise Challenge(self)

        self.check_header(auth)
        self.check_nonce(auth)

        hA1 = self.get_key(auth.username)
        hA2 = hash_all(request.method, auth.uri)

        if hA1 is None:
            raise Unauthorized()

        if auth.response != digest(hA1, hA2):
            raise Unauthorized()

    def check_header(self, auth):
        uri = request.path
        if request.query_string:
            uri += '?' + request.query_string

        bad_uri = auth.uri != uri
        bad_qop = auth.qop != self.qop

        incomplete = any(param is None for param in [
            auth.response,
            auth.username,
            auth.nonce,
            auth.cnonce,
            auth.nc,
            auth.uri,
            auth.qop
        ])

        if incomplete or bad_uri or bad_qop:
            raise BadRequest()

    def check_nonce(self, auth):
        token = self.tokens.get(auth.nonce, None)
        nc = int(auth.nc, 16)
        ip = request.remote_addr

        if token is None or token.stale():
            raise Challenge(self, True)

        if ip != token.ip or nc in token.used:
            raise Unauthorized()

        token.used.add(nc)

    def gen_nonce(self):
        while True:
            nonce = encode(urandom(8), 'hex').decode()
            if nonce not in self.tokens or self.tokens[nonce].stale():
                break

        self.tokens[nonce] = Token()
        self.maid.clean(self.tokens)
        return nonce

    def add_headers(self, response):
        response = make_response(response)
        auth = request.authorization

        hA1 = self.get_key(auth.username)
        hA2 = hash_all('', auth.uri)
        rspauth = digest(hA1, hA2)

        response.headers['Authentication-Info'] = dump_header({
            'rspauth': rspauth,
            'qop': auth.qop,
            'cnonce': auth.cnonce,
            'nc': auth.nc,
        })

        return response
