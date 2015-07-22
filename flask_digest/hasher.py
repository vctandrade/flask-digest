from hashlib import md5
from flask import request

def hash_all(*args):
    strings = map(str, args)
    hashed = md5(':'.join(strings))
    return hashed.hexdigest()

def digest(hA1, auth):
    auth_int = str(auth.qop) == 'auth-int'
    hA2 = build_hA2(request.get_data() if auth_int else None, auth)
    return hash_all(hA1, auth.nonce, auth.nc, auth.cnonce, auth.qop, hA2)

def build_hA2(content_md5, auth):
    if content_md5 is None: return hash_all(request.method, auth.uri)
    return hash_all(request.method, auth.uri, content_md5)
