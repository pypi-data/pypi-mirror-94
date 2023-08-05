from django.contrib import admin
from django.conf import settings

if settings.OBJECTSYNCER_ROLE == 'SERVER':
    from .models import Application, JobChange

    admin.site.register(Application)
    admin.site.register(JobChange)
