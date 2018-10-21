from django.db import models


class ReceivedFax(models.Model):

    created = models.DateField(auto_now=True)
    media_url = models.TextField(default='')
    num_pages = models.IntegerField(default=1)
