import datetime as dt
from typing import final, override

from dmr.plugins.msgspec import MsgspecSerializer
from dmr.security.jwt.views import (
    ObtainTokensPayload,
    ObtainTokensResponse,
    ObtainTokensSyncController,
)


@final
class ObtainTaskTokens(
    ObtainTokensSyncController[
        MsgspecSerializer,
        ObtainTokensPayload,
        ObtainTokensResponse,
    ],
):
    """Issue access and refresh tokens for a Django user."""

    @override
    def convert_auth_payload(
        self,
        payload: ObtainTokensPayload,
    ) -> ObtainTokensPayload:
        """Pass the credentials to Django's authentication backend."""
        return payload

    @override
    def make_api_response(self) -> ObtainTokensResponse:
        """Return signed tokens for the authenticated user."""
        now = dt.datetime.now(dt.UTC)
        return {
            'access_token': self.create_jwt_token(
                expiration=now + self.jwt_expiration,
                token_type='access',  # noqa: S106
            ),
            'refresh_token': self.create_jwt_token(
                expiration=now + self.jwt_refresh_expiration,
                token_type='refresh',  # noqa: S106
            ),
        }
