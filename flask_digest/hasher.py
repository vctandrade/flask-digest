import hashlib

def hash_all(*args):
    strings = map(str, args)
    hashed = hashlib.md5(':'.join(strings))
    return hashed.hexdigest()

def digest(request, hA1):
    auth = request.authorization
    hA2 = hash_all(request.method, auth.uri)
    return hash_all(hA1, auth.nonce, auth.nc, auth.cnonce, auth.qop, hA2)
