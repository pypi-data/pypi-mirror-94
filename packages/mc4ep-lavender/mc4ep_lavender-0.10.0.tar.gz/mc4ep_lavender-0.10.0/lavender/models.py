from functools import partial
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now

from lavender import texture


class Player(AbstractUser):
    packages = models.ManyToManyField('Package', blank=True)


class LogHistory(models.Model):
    player: Player = models.ForeignKey(Player, on_delete=models.CASCADE)

    date = models.DateTimeField(default=now)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.player.username} at {self.date} from {self.source}"


class Token(models.Model):
    player: Player = models.OneToOneField(Player, on_delete=models.CASCADE)

    access = models.CharField(max_length=32, null=True)
    client = models.CharField(max_length=32, null=True)
    uuid = models.UUIDField(default=uuid4)
    server_id = models.CharField(max_length=48, null=True)
    created = models.DateTimeField(default=now)

    def __repr__(self):
        return f"{self.player.username} (access: {self.access} client: {self.client}"


class GameLog(models.Model):
    player: Player = models.ForeignKey(Player, on_delete=models.CASCADE)

    date = models.DateTimeField(default=now)
    kind = models.CharField(max_length=16)
    payload = models.TextField(default="")

    def __str__(self):
        return f"{self.player.username} at {self.date}: {self.kind}"


class Package(models.Model):
    name = models.CharField(max_length=16)
    version = models.CharField(max_length=16)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Quenta(models.Model):
    player: Player = models.OneToOneField(Player, on_delete=models.CASCADE, null=True)

    text = models.TextField()
    comments = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        status = "approved" if self.approved else "declined"
        return f"{self.__class__.__name__} for {self.player.username}: {status}"


class Wardrobe(models.Model):
    player: Player = models.ForeignKey(Player, on_delete=models.CASCADE)

    skin_height = models.PositiveIntegerField(null=True)
    skin_width = models.PositiveIntegerField(null=True)
    skin = models.ImageField(null=True, blank=True, height_field='skin_height', width_field='skin_width',
                             upload_to=partial(texture.path_handler, texture.TextureType.SKIN),
                             storage=texture.OverwriteStorage())

    cloak_height = models.PositiveIntegerField(null=True)
    cloak_width = models.PositiveIntegerField(null=True)
    cloak = models.ImageField(null=True, blank=True, height_field='cloak_height', width_field='cloak_width',
                              upload_to=partial(texture.path_handler, texture.TextureType.CLOAK),
                              storage=texture.OverwriteStorage())

    elytra_height = models.PositiveIntegerField(null=True)
    elytra_width = models.PositiveIntegerField(null=True)
    elytra = models.ImageField(null=True, blank=True, height_field='elytra_height', width_field='elytra_width',
                               upload_to=partial(texture.path_handler, texture.TextureType.ELYTRA),
                               storage=texture.OverwriteStorage())

    def __str__(self):
        return f"{self.__class__.__name__} for {self.player.username}"


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    record = LogHistory(player=user, source='site')
    record.save()
