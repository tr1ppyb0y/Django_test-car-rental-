from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


@database_sync_to_async
def get_user(headers):
    AuthError = AuthenticationFailed
    try:
        auth_header_token = headers[b'authorization'].decode()
    except UnicodeError:
        raise AuthError(_("Invalid token header: Authorization key is not present!"))
    try:
        name, key = auth_header_token.split()
        if name == 'Token':
            token = Token.objects.get(token_key=key[:8])
            return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            scope['user'] = await get_user(headers)
        return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))