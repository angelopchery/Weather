from django.db import models

# Create your models here.
class History(models.Model):
    city = models.TextField(default='')
    country_code = models.TextField()
    coordinate = models.CharField(max_length=20)
    temp = models.CharField(max_length=20)
    pressure = models.DecimalField(max_digits = 10, decimal_places = 2)
    humidity = models.DecimalField(max_digits = 10, decimal_places = 2)
    timestamp = models.DateTimeField(auto_now_add = True)
