from django.db import models


class Version(models.Model):
    app_version = models.IntegerField()
