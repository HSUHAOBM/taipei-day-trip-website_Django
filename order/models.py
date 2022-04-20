from django.db import models

# Create your models here.
class order(models.Model):

    user_id = models.IntegerField()
    trip_id = models.IntegerField()
    trip_date = models.DateTimeField()
    trip_time = models.TextField()
    trip_cost = models.IntegerField()
    contact_name = models.TextField()
    contact_email = models.TextField()
    contact_phone= models.IntegerField()
    payment = models.TextField()
    prime = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order"