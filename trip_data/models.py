from django.db import models

# Create your models here.
class Trip_data(models.Model):
    stitle = models.TextField()
    category = models.TextField(blank=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    transport = models.TextField(blank=True,null=True)
    mrt = models.TextField(blank=True,null=True)
    latitude = models.TextField(blank=True,null=True)
    longitude = models.TextField(blank=True,null=True)
    images = models.TextField(blank=True,null=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "trip_data"
