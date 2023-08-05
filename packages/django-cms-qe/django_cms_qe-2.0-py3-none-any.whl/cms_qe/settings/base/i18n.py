"""
Internationalization settings for Django app.
"""

from django.utils.translation import ugettext_lazy as _

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _(u'English')),
)

LOCALE_PATHS = (
    'locale',
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
