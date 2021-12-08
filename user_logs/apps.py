from django.apps import AppConfig


class UserLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_logs'
    
    def ready(self) -> None:
        import user_logs.signals
        return super().ready()
