"""
Test Django settings for eox_tagging project.
"""
from __future__ import unicode_literals

from .common import *  # pylint: disable=wildcard-import


class SettingsClass:
    """ dummy settings class """


SETTINGS = SettingsClass()
# This is executing the plugin_settings method imported from common module
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
INSTALLED_APPS = vars().get("INSTALLED_APPS", [])
TEST_INSTALLED_APPS = [
    "django.contrib.sites",
]
for app in TEST_INSTALLED_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

# For testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

ROOT_URLCONF = 'eox_tagging.urls'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_TZ = True

ALLOWED_HOSTS = ['*']


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.EOX_TAGGING_SKIP_VALIDATIONS = True
    settings.EOX_TAGGING_LOAD_PERMISSIONS = False
    settings.EOX_TAGGING_BEARER_AUTHENTICATION = 'eox_tagging.edxapp_wrappers.backends.bearer_authentication_i_v1_test'
    settings.DATA_API_DEF_PAGE_SIZE = 1000
    settings.DATA_API_MAX_PAGE_SIZE = 5000
    settings.TEST_SITE = 1


SETTINGS = SettingsClass()
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
