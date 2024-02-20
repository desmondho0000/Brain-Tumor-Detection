from django.db import models
from django.utils import timezone

# Create your models here.
class Prediction(models.Model):
    username = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='predicted_images/')
    prediction_result = models.CharField(max_length=100)
    confidence = models.FloatField()


    def __str__(self):
        return f"Prediction for {self.patient_name} by {self.username}"