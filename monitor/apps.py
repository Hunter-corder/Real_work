from django.apps import AppConfig

class MonitorConfig(AppConfig):
    name = 'monitor'

    def ready(self):
        # Import the necessary functions inside the ready method
        # to avoid circular imports before the app registry is ready
        from .views import start_background_task
        start_background_task()
