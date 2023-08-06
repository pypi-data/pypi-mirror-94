from typing import Optional, Tuple

from ._base import ConfigMixin


class HttpsMixin(ConfigMixin):
    """Configure Django's security middleware for HTTPS."""

    SECURE_SSL_REDIRECT = True

    # This must be set when deployed behind a proxy
    SECURE_PROXY_SSL_HEADER: Optional[Tuple[str, str]] = None

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Enable HSTS
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 365  # 1 year
    # This is already False by default, but it's important to ensure HSTS is not forced on other
    # subdomains which may have different HTTPS practices.
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
