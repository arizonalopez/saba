from django.apps import AppConfig


class TutorsConfig(AppConfig):
    name = 'tutors'
    verbose_name = 'Tutors'

    def ready(self):
        from .signal import inform_administrators
        from .checks import settings_check
