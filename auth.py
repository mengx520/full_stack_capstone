from os import environ
import json
import os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'xiaohan.us.auth0.com'
API_AUDIENCE = 'casting_agency'
ALGORITHMS = ["RS256"]

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
implement get_token_auth_header() method
'''


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    https://auth0.com/docs/quickstart/backend/python/01-authorization
    """
    auth = request.headers.get('Authorization', None)
    # raise an AuthError if no header is present
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"}, 401)

    # split bearer and token
    parts = auth.split()

    # raise an AuthError if no header is present
    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer"}, 401)

    # raise an AuthError if the header is malformed
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"}, 401)

    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token"}, 401)

    # return the token part of the header
    token = parts[1]
    return token


'''
implement check_permissions(permission, payload) method
https://auth0.com/docs/tokens/access-tokens/validate-access-tokens
'''


def check_permissions(permission, payload):
    # check payload contains permission key
    if 'permissions' not in payload:
        abort(400)
    # raise an AuthError if the requested permission string is not in the
    # payload permissions array
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unauthorized',
            'description': "You don't have access to this resource"}, 403)
    return True


'''
implement verify_decode_jwt(token) method
'''


def verify_decode_jwt(token):
    # Retrieve the public key from Auth0 Discovery endpoint
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # Extract the JWT from the request's authorization header
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    # key id must exist in token
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # verify token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 401)


'''
implement @requires_auth(permission) decorator method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                # if "UNITTEST" not in os.environ:
                payload = verify_decode_jwt(token)
                # else:
                # payload = {}
            except BaseException:
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
