from django.core.checks import Error, register, Tags

@register(Tags.compatibility)
def settings_check(app_configs, **kwargs):
    from django.conf import settings
    errors = []
    if not settings.LOGIN_URL:
        errors.append(Error(
            'The login uri is not set in the project settings',
            hint='''in order to restrict some pages to the authenticated user, define settings 'like LOGIN_URL=/tutors/login' in your settings''', id='tutors.W001'
        ))
    return errors