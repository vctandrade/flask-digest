from werkzeug.exceptions import Unauthorized

class Challenge(Unauthorized):
    def __init__(self, stomach, stale=False):
        Unauthorized.__init__(self)

        realm = stomach.realm
        nonce = stomach.gen_nonce()
        qop = stomach.qop

        self.info = (realm, nonce, [qop], None, 'MD5', stale)

    def get_response(self, environ=None):
        response = Unauthorized.get_response(self, environ)
        response.www_authenticate.set_digest(*self.info)
        return response
