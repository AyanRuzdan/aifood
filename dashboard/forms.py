from django import forms
from django.contrib.auth.models import User
from .models import FoodItem, Monitoring


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'weight', 'temperature',
                  'humidity', 'location']
class MonitoringForm(forms.ModelForm):
    class Meta:
        model = Monitoring
        fields = ['food_item', 'current_temperature',
                  'current_humidity', 'current_location']
