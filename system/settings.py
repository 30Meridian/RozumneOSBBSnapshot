# coding: utf-8
import os
from machina import get_apps as get_machina_apps, MACHINA_MAIN_TEMPLATE_DIR, MACHINA_MAIN_STATIC_DIR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ''  # Generate own secret key for your instance
CRON_SECRET = ''  # Generate secret for cron view urls

DEBUG = True
TEMPLATE_DEBUG = DEBUG


if(DEBUG):
    ALLOWED_HOSTS = ['127.0.0.1','192.168.86.1']
    INTERNAL_IPS=['192.168.86.1','127.0.0.1']
else:
    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS=['*']

# Application definition
#
INSTALLED_APPS = [ #Don't forget to add locale in module's locale list below
    'suit',
    # 'django.contrib.admin',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'system',
    'defects',
    'news',
    'ideas',
    'polls',
    'problems',
    'allauth',
    'allauth.account',
    'pure_pagination',
    'django_activeurl',
    'ckeditor_uploader',
    'stronghold',
    'common',
    'newsletter',
    'condominium_management',
    'finance',
    'cms',
    'filemanager',
    'nested_admin',
    # Machina related apps:
    'mptt',
    'haystack',
    'widget_tweaks',
    'django_markdown',
    # Gallery:
    'photologue',
    'sortedm2m',
    #blog
    'blog'
] + get_machina_apps()


HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
    'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
  },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'system.cp.CondominiumSessionMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
    'system.middleware.UserRequiredMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
)

AUTH_USER_MODEL="system.User"

# migth need to disable this leter
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'system.urls'


TEMPLATE_DIRS = (
  MACHINA_MAIN_TEMPLATE_DIR,
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'system.cp.condominium_temp',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.template.context_processors.i18n',
    'machina.core.context_processors.metadata',
)
WSGI_APPLICATION = 'system.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': BASE_DIR+'/system/'+'mysqldb.conf',
        },
    }
}

TIME_ZONE = 'Europe/Kiev'
LANGUAGE_CODE = 'uk_UA'
DEFAULT_CHARSET = 'utf8'
USE_I18N = True
DATETIME_FORMAT = 'M. d, Y H:i'

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('uk_UA', _('Ukrainian')),
    ('ru', _('Russian')),
    ('nl', _('Dutch')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'modules/allauth/locale'),
    os.path.join(BASE_DIR, 'modules/blog/locale'),
    os.path.join(BASE_DIR, 'modules/newsletter/locale'),
    os.path.join(BASE_DIR, 'modules/machina/locale'),
    os.path.join(BASE_DIR, 'applications/polls/locale'),
    os.path.join(BASE_DIR, 'modules/filemanager/locale'),
    os.path.join(BASE_DIR, 'applications/condominium_management/locale'),
    os.path.join(BASE_DIR, 'applications/defects/locale'),
    os.path.join(BASE_DIR, 'applications/finance/locale'),
    os.path.join(BASE_DIR, 'applications/news/locale'),
    os.path.join(BASE_DIR, 'applications/ideas/locale'),
    os.path.join(BASE_DIR, 'applications/finance/locale'),
    os.path.join(BASE_DIR, 'applications/cms/locale'),
    os.path.join(BASE_DIR, 'applications/problems/locale'),
)


STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    MACHINA_MAIN_STATIC_DIR,
    ]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

GOOGLE_API_KEY=''

#for alloauth module
SITE_ID = 1
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DJANGORESIZED_DEFAULT_SIZE = [150, 75]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = "/confirmyouremail"
ACCOUNT_SIGNUP_FORM_CLASS = 'system.forms.SignupForm'
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = '/'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#SMTP settings
EMAIL_USE_SSL= True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''
DEFAULT_TO_EMAIL = ''
TIMEOUT = 1

#Pagination
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 2,
    'MARGIN_PAGES_DISPLAYED': 1,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

CKEDITOR_CONFIGS = {
    'default': {
         'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
              '-', 'Image', 'Link', 'Unlink', 'Anchor',
              '-', 'Format',
              '-', 'SpellChecker', 'Scayt',
              '-', 'Maximize',
            ],
            [      'HorizontalRule',
              '-', 'Table'
              '-', 'Iframe',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
              '-', 'SpecialChar',
              '-', 'Source',
              '-', 'About',
            ]
        ],
        'height': 300,
        'width': 650,
        'extraAllowedContent': 'iframe[*]',
    },
}

CKEDITOR_UPLOAD_PATH = "news/content/"
CKEDITOR_IMAGE_BACKEND = 'pillow'

ADMINS = ()
MANAGERS = ADMINS


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR+'/static/django_cache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR+'/static/tmp',
    }
}


KARMA = {
    'SIGNUP': 5,
    'IDEA_WAS_APPROVE': 10,
    'IDEA_VOTE': 1,
    'IDEA_DISVOTE': -1,
    'IDEA_ONCONSIDERATION': 30,
    'DEFECT_WAS_APPROVE': 5,
    'DEFECT_COMMENT': 1,
    'DEFECT_COMMENT_BLOCK': -5,
}

SUIT_CONFIG = {
    'ADMIN_NAME':  _('OUR_OSBB'),
    'LIST_PER_PAGE': 15,
}

CKEDITOR_ALLOW_NONIMAGE_FILES = False

STRONGHOLD_DEFAULTS = True
STRONGHOLD_PUBLIC_URLS = (
    r'^/accounts/login/$',
    r'^/accounts/signup/$',
    r'^/accounts/password/reset/$',
    r'^/accounts/password/reset/done/$',
    r'^/jsi18n/$',
    r'^/help/$',
    r'^/contacts$',
    r'^/about/$',
    r'^/instructions/$',
    r'^/$',
    r'^/index/',
)