"""
ASGI config for chan project.
<<<<<<< HEAD

It exposes the ASGI callable as a module-level variable named ``application``.

=======
It exposes the ASGI callable as a module-level variable named ``application``.
>>>>>>> 5431355000ea1ad6f9b9220c10644b1fe4c0b3a3
For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone.settings')

<<<<<<< HEAD
application = get_asgi_application()
=======
application = get_asgi_application()
>>>>>>> 5431355000ea1ad6f9b9220c10644b1fe4c0b3a3
