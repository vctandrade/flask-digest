from werkzeug.exceptions import HTTPException
from werkzeug import Response, WWWAuthenticate

class Challenge(HTTPException):
    code = 401
    description = '''
        <h1> Challenge </h1>
        To gain access to this resource, you must first provide the server with your credentials.
        If they already were provided, make sure your validation token hasn't expired.
    '''

    def __init__(self, stomach, stale=False):
        self.www_authenticate = WWWAuthenticate()
        self.www_authenticate.set_digest(stomach.realm, stomach.gen_nonce(), [stomach.qop], stale=stale)
        self.www_authenticate = self.www_authenticate.to_header()

    def get_response(self, environ=None):
        response = Response(self.description, self.code, content_type='html')
        response.headers['Access-Control-Expose-Headers'] = 'WWW-Authenticate'
        response.headers['WWW-Authenticate'] = self.www_authenticate
        return response
