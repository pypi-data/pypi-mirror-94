from django.conf import settings

AUTH_API_ENABLED = getattr(settings, 'LAVENDER_AUTH_API_ENABLED', False)
LEGACY_AUTH_API_ENABLED = getattr(settings, 'LAVENDER_LEGACY_AUTH_API_ENABLED', False)
LEGACY_AUTH_FAIL_MESSAGE = getattr(settings, 'LAVENDER_LEGACY_AUTH_FAIL_MESSAGE', 'Failed to login')
AUTH_POSTPROCESS_CLASS = getattr(settings, 'LAVENDER_AUTH_POSTPROCESS_CLASS', None)
