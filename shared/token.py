from rest_framework.authtoken.models import Token

from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone


class AuthToken:

    def __init__(self):
        self.ttl = settings.DRF_TOKEN_TTL

    def expires_in(self, token):
        return timedelta(seconds=self.ttl) - (timezone.now() - token.created)

    def is_expired(self, token):
        token = Token.objects.filter(key=token).first()
        if not token:
            return True
        return self.expires_in(token) < timedelta(seconds=0)

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        if self.is_expired(token):
            token.delete()
            token = Token.objects.create(user=token.user)
        return token.key


def authorization(function):
    def wrap(request, *args, **kwargs):
        auth = None
        user = None
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION']

        if auth:
            token = Token.objects.filter(key=auth).first()
            if token:
                user = User.objects.filter(
                    username=token.user.username).first()
        if not user:
            return JsonResponse({
                "error": "Invalid Authentication"
            }, safe=False, status=401)

        if not user.is_active:
            return JsonResponse({
                "error": "User is disabled"
            }, safe=False, status=403)

        request.user = user

        return function(request, *args, **kwargs)
    return wrap
