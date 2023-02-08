from django.apps import AppConfig
import sys


class DevicecontrollerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deviceController'

#    def ready(self):
#        if 'runserver' not in sys.argv:
#            return True
#        # you must import your modules here
#        # to avoid AppRegistryNotReady exception
#        # startup code here
#
