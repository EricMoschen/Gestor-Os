from dotenv import load_dotenv
import os
from pathlib import Path
import dj_database_url
from django.contrib.messages import constants
load_dotenv()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = os.environ.get('SECRET_KEY', 'chave-fallback-para-dev')

DEBUG = False

ALLOWED_HOSTS = ['gestor-os.onrender.com']  

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuario',
    'menuos',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


BASE_DIR = Path(__file__).resolve().parent.parent
# Banco de dados - PostgreSQL via dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3'  # Usado caso DATABASE_URL não esteja definida
    )
}

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Diretório para arquivos estáticos coletados
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Campo padrão para chaves primárias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login e redirecionamento
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/menuos/'

# Estilo de mensagens Django
MESSAGE_TAGS = {
    constants.SUCCESS: 'bg-green-50 text-green-700',
    constants.ERROR: 'bg-red-50 text-red-700'
}

# Configurações de sessão
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Segurança adicional para produção
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True