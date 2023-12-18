from django.db import models
from django.conf import settings


class PredictionResult(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    prediction_datetime = models.DateTimeField()

