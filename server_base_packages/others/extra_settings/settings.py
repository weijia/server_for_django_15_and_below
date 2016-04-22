INSTALLED_APPS += (
    'bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # 'south',  # Do not work in SAE
    # 'mptt',
    # 'treenav',
    # 'background_task',
    # 'django_cron',  # Do not work in SAE
    # 'jquery_ui',
    # 'provider',
    # 'provider.oauth2',
    'simplemenu',
    'webmanager',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'extra_settings.urls'

AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend', 'guardian.backends.ObjectPermissionBackend')

ANONYMOUS_USER_ID = -1