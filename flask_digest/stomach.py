from time import time
from os import urandom
from flask import request
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized
from functools import wraps

from hasher import digest, hash_all
from challenge import Challenge
from cleaning import Maid

#TODO log attacks
#TODO implement auth-int
#TODO add Authentication-Info
#TODO per resource permission
#TODO allow blueprints and views

class Token(object):
    def __init__(self):
        self.IP = request.remote_addr
        self.timer = time()
        self.nc = 0

    def stale(self):
        return time() - self.timer > 1800

class Stomach(object):

    def __init__(self, realm):
        self.realm = realm
        self.tokens = dict()
        self.clean = Maid()
        self.qop = 'auth'

    def access(self, func):
        self.get_key = func
        return func

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
            return func(*args, **kargs)
        return wrapper

    def get_key(self, username):
        return None

    def authenticate(self):
        auth = request.authorization
        if auth is None: raise Challenge(self, stale=False)

        self.check_header(auth)
        self.check_nonce(auth)

        hash_pass = self.get_key(auth.username)
        if hash_pass is None: raise Unauthorized()

        if auth.response != digest(request, hash_pass):
            raise Unauthorized()

    def gen_nonce(self):
        while True:
            nonce = urandom(8).encode('hex')
            if nonce not in self.tokens: break
            if self.tokens[nonce].stale(): break
        self.tokens[nonce] = Token()
        self.clean(self.tokens)
        return nonce

    def check_header(self, auth):
        uri = request.path
        if request.query_string:
            uri += '?' + request.query_string

        bad_uri = auth.uri != uri
        bad_qop = str(auth.qop) != self.qop

        incomplete = any(param == None for param in [
            auth.response, auth.username,
            auth.nonce, auth.cnonce, auth.nc,
            auth.uri, auth.qop
        ])

        if incomplete or bad_uri or bad_qop:
            raise BadRequest()

    def check_nonce(self, auth):
        nonce = auth.nonce
        nc = int(auth.nc, 16)
        IP = request.remote_addr

        if nonce in self.tokens and self.tokens[nonce].stale():
            del self.tokens[nonce]
        token = self.tokens.get(nonce, None)

        if token == None: raise Challenge(self, stale=True)
        if IP != token.IP: raise Unauthorized()
        if nc <= token.nc: raise Unauthorized()
        token.nc = nc
