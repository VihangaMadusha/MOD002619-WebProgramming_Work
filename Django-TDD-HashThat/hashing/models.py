from django.db import models


class Hash(models.Model):
    text = models.TextField()
    # SHA256 gives a 256-bit hash = 64 hex characters
    hash = models.CharField(max_length=64)
