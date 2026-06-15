"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
# from django.contrib.auth import get_user_model
#
# def create_superuser():
#     User = get_user_model()
#     if not User.objects.filter(username=os.getenv("DJANGO_SUPERUSER_USERNAME")).exists():
#         User.objects.create_superuser(
#             username=os.getenv("DJANGO_SUPERUSER_USERNAME"),
#             email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
#             password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
#         )
#
# try:
#     create_superuser()
# except:
#     pass