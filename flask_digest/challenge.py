from werkzeug.exceptions import Unauthorized
from werkzeug import WWWAuthenticate

class Challenge(Unauthorized):

    def __init__(self, stomach, stale=False):
        Unauthorized.__init__(self)

        realm = stomach.realm
        nonce = stomach.gen_nonce()
        qop = [stomach.qop]

        self.challenge = WWWAuthenticate()
        self.challenge.set_digest(realm, nonce, qop, stale)

    def get_response(self, environ=None):
        response = Unauthorized.get_response(self)
        response.headers['Access-Control-Expose-Headers'] = 'WWW-Authenticate'
        response.headers['WWW-Authenticate'] = self.challenge.to_header()
        return response
