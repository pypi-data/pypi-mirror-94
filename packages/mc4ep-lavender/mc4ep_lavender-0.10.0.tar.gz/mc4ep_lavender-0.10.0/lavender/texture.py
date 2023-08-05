from enum import Enum
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class TextureType(Enum):
    SKIN = "skin"
    CLOAK = "cloak"
    ELYTRA = "elytra"


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            Path(settings.MEDIA_ROOT, name).unlink()
        return name


def path_handler(texture_type: TextureType, instance, filename: str) -> str:
    return f'{texture_type.value}s/{instance.player.username}.png'
