from typing import Optional
from uuid import UUID
from flask_httpauth import HTTPTokenAuth

from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature

from valhalla.utils import SECRET_KEY, TOKEN_EXPIRE
from werkzeug.exceptions import Unauthorized


auth = HTTPTokenAuth()


def generate_auth_token(*, uuid: UUID):
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=TOKEN_EXPIRE)
    return serializer.dumps({'uuid': uuid.hex})


@auth.error_handler
def auth_failed():
    raise Unauthorized(description="Authentication failed")


@auth.verify_token
def verify_auth_token(token) -> Optional[UUID]:
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)
    try:
        data = serializer.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    else:
        return UUID(data['id'])
