from django.db import models


class Item(models.Model):
    status = models.CharField(max_length=200, default="pending")
    item = models.CharField(max_length=200)

    def __str__(self):
        return self.item
