from django.db import models
from django.contrib.auth.models import User


class FoodItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Monitoring(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    current_temperature = models.FloatField()
    current_humidity = models.FloatField()
    current_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Safe')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_item.name} - {self.status}"
