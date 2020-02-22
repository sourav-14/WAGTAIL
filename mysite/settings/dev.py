from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vi@pr&9$4a=oz8h$@jslng%j&pj7)0^i_z4iguq=z220@uxda#'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE =  MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
    'wagtail.contrib.styleguide'
]

INTERNAL_IPS = ["127.0.0.1"]

#CACHES = {
 #   "default": {
  #      "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
   #     "LOCATION" :  "/home/sourav/projects/WAGTAILCMS/mysite/cache"
    #}
#}

try:
    from .local import *
except ImportError:
    pass
