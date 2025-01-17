import jwt

from rest_framework import authentication, exceptions 
from django.conf import settings

from .models import Auth


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request).decode('utf-8')

        if not auth_data or not auth_data.startswith('Bearer '):
            return None

        token = auth_data.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = Auth.objects.filter(email=payload['email']).first()

            if user is None:
                raise exceptions.AuthenticationFailed('User not found')
            return (user, None)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')


def generate_jwt_token(useremail):
    payload = {
        'email': useremail
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token    

def auth_by_token(request):
    try:
        jwt_auth= JWTAuthentication()
        auth= jwt_auth.authenticate(request)
        if auth:
            return auth[0]
        else:
            return None
    except exceptions.AuthenticationFailed:
        return exceptions.AuthenticationFailed
    


    

