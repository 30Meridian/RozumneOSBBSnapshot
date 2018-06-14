from django.db import models
from system.models import User

class Items(models.Model):
    user_ref = models.ForeignKey(User, db_column='user_ref', on_delete=models.CASCADE)
    pay_for = models.CharField(max_length=1000)
    datatime_create = models.DateTimeField(auto_now_add=True)
    datetime_pay = models.DateTimeField()
    amount = models.IntegerField()

    class Meta:
        managed = True