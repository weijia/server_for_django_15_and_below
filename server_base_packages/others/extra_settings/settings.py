INSTALLED_APPS += (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'south',  # Do not work in SAE
    #'mptt',
    #'treenav',
    #'background_task',
    #'django_cron',  # Do not work in SAE
    #'jquery_ui',
    #'provider',
    #'provider.oauth2',
    'webmanager',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'extra_settings.urls'
