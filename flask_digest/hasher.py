from flask import request
from hashlib import md5

def hash_all(*args):
    strings = map(str, args)
    encoded = ':'.join(strings).encode('utf-8')
    return md5(encoded).hexdigest()

def digest(hA1, hA2):
    auth = request.authorization
    return hash_all(hA1, auth.nonce, auth.nc, auth.cnonce, auth.qop, hA2)
