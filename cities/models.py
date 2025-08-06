from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)
    humidity = models.IntegerField()
    wind = models.FloatField()
    date_checked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather in {self.city} at {self.date_checked.strftime('%Y-%m-%d %H:%M')}"
