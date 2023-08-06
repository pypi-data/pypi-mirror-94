from pathlib import Path
from typing import Type

from configurations import values

from ._base import ComposedConfiguration, ConfigMixin


class StaticFileMixin(ConfigMixin):
    """
    Configure static file collection by Django, with serving in development.

    This could be used directly, but is typically included implicitly by WhitenoiseStaticFileMixin.

    Downstreams must explicitly define the settings:
    * `BASE_DIR`, as the pathlib Path to the project root. This can typically be done as:
      `BASE_DIR = Path(__file__).resolve(strict=True).parent.parent`.
    """

    STATIC_URL = '/static/'

    # BASE_DIR is in Django's startproject template, but isn't actually used as a real setting
    @property
    def BASE_DIR(self) -> Path:  # noqa: N802
        raise Exception('BASE_DIR must be explicitly set to the path of the Django project root.')

    @property
    def STATIC_ROOT(self):  # noqa: N802
        # Django staticfiles creates any intermediate directories which don't exist
        # TODO: allow from env?
        return values.PathValue(
            str(Path(self.BASE_DIR) / 'staticfiles'),
            environ=False,
            check_exists=False,
            # Disable late_binding, to make this return an actual str, not a Value, since some
            # "os" module functions (which are called with this) do strict nominal type checking.
            late_binding=False,
        )

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        configuration.INSTALLED_APPS += ['django.contrib.staticfiles']


class WhitenoiseStaticFileMixin(StaticFileMixin):
    """
    Configure static file serving with Whitenoise for development and production.

    The package `whitenoise[brotli]` must be installed.
    """

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]) -> None:
        # Insert immediately before staticfiles app
        staticfiles_index = configuration.INSTALLED_APPS.index('django.contrib.staticfiles')
        configuration.INSTALLED_APPS.insert(staticfiles_index, 'whitenoise.runserver_nostatic')

        # Insert immediately after SecurityMiddleware
        try:
            security_index = configuration.MIDDLEWARE.index(
                'django.middleware.security.SecurityMiddleware'
            )
        except ValueError:
            raise Exception(
                'WhitenoiseStaticFileMixin must be loaded after '
                'the SecurityMiddleware is added to MIDDLEWARE.'
            )
        configuration.MIDDLEWARE.insert(
            security_index + 1, 'whitenoise.middleware.WhiteNoiseMiddleware'
        )

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
