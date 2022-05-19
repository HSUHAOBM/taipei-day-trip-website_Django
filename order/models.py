from django.db import models
from member.models import Member
from trip_data.models import Trip_data

# Create your models here.
class Order(models.Model):
    user_id = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
    )
    trip_id = models.OneToOneField(
        Trip_data,
        on_delete=models.CASCADE,
    )
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