from django.db import models
from member.models import Member
from trip_data.models import Trip_data

# Create your models here.
class Order(models.Model):
    user_id = models.ForeignKey(
        'member.Member',
        on_delete=models.CASCADE,null=True)
    trip_id = models.ForeignKey(
        'trip_data.Trip_data',
        on_delete=models.CASCADE,null=True)
    trip_date = models.DateTimeField(null=True)
    trip_time = models.TextField(null=True)
    trip_cost = models.IntegerField(null=True)
    contact_name = models.TextField(null=True)
    contact_email = models.TextField(null=True)
    contact_phone= models.TextField(null=True)
    payment = models.TextField(null=True)
    prime = models.TextField(null=True)
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order"