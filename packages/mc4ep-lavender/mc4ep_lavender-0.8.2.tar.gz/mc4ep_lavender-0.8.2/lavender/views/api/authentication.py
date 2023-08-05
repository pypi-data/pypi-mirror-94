from importlib import import_module
from typing import Optional

from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404

from lavender import settings
from lavender.models import LogHistory, Player


def _postprocess(user: Optional[Player]) -> bool:
    if user is None:
        return False

    if settings.AUTH_POSTPROCESS_CLASS is None:
        return True

    module_name, class_name = settings.AUTH_POSTPROCESS_CLASS.rsplit(".", 1)
    module = import_module(module_name)
    assert hasattr(module, class_name), f"Class {class_name} is not in {module_name}"
    checker = getattr(module, class_name)()
    return checker.check(user)


def _auth(username, password, handler):
    user = authenticate(username=username, password=password)
    if user:
        record = LogHistory(player=user, source='game')
        record.save()

    return handler(_postprocess(user))


def auth(request, username, password):
    if not settings.AUTH_API_ENABLED:
        raise Http404

    def handler(success: bool) -> HttpResponse:
        status: int = success and 204 or 403
        return HttpResponse(status=status)

    return _auth(username, password, handler)


def auth_legacy(request, username, password):
    if not settings.LEGACY_AUTH_API_ENABLED:
        raise Http404

    def handler(success: bool) -> HttpResponse:
        if success:
            message = f"OK:{username}"
        else:
            message = settings.LEGACY_AUTH_FAIL_MESSAGE
        return HttpResponse(message)

    return _auth(username, password, handler)
