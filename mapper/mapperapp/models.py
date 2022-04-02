from django.db import models

class coords(models.Model):
    username = models.CharField(max_length = 255, default = 0)
    access_token = models.CharField(max_length = 255, default = 0)
    website_id = models.CharField(max_length = 255, default = 0)
    lat = models.CharField(max_length = 255, default = 0)
    long = models.CharField(max_length = 255, default = 0)
    city = models.CharField(max_length = 255, default = 0)
    state = models.CharField(max_length = 255, default = 0)
    country = models.CharField(max_length = 255, default = 0)
    ip_address = models.CharField(max_length = 255, default = 0)

    def __str__(self):
        return self.username

class registeredWebsite(models.Model):
    username = models.CharField(max_length = 255, default = 0)
    website = models.CharField(max_length = 255, default = 0)

    def __str__(self):
        return self.username + ' - ' + self.website
