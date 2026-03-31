"""
Production settings for Rapid Cash
"""
from .settings import *
import os
import sys

# SECURITY SETTINGS FOR PRODUCTION
DEBUG = False

# Generate secure secret key in production
SECRET_KEY = os.environ.get('SECRET_KEY')

# Restrict allowed hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Check if running collectstatic (build phase)
IS_COLLECTSTATIC = 'collectstatic' in sys.argv

# Database configuration for production
if IS_COLLECTSTATIC:
    # Use dummy SQLite for collectstatic during build (no DB needed)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    # Real PostgreSQL config for runtime using DATABASE_URL
    import os
    import dj_database_url
    
    # Get DATABASE_URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Parse DATABASE_URL
        DATABASES = {
            'default': dj_database_url.parse(database_url, conn_max_age=600)
        }
    else:
        # Fallback (should not happen in production)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME', 'rapid_cash'),
                'USER': os.environ.get('DB_USER', 'postgres'),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': os.environ.get('DB_HOST', 'localhost'),
                'PORT': os.environ.get('DB_PORT', '5432'),
            }
        }

# Redis Cache configuration (Fly.io Redis or Upstash)
REDIS_URL = os.environ.get('REDIS_URL', os.environ.get('FLY_REDIS_CACHE_URL', 'redis://localhost:6379/1'))
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# Celery configuration for Fly.io
CELERY_BROKER_URL = os.environ.get('REDIS_URL', os.environ.get('FLY_REDIS_CACHE_URL', 'redis://localhost:6379/0'))
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', os.environ.get('FLY_REDIS_CACHE_URL', 'redis://localhost:6379/0'))

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'rapid_cash': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Ensure logs directory exists
import os
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
