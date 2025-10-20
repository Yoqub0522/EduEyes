from common.models import BaseModel
from django.db import models



class Address(BaseModel):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    street_name = models.CharField(max_length=1000, null=True, blank=True)



    class Meta:
        db_table = "addresses"
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=['lat', 'long']),
        ]
        unique_together = ('lat', 'long')

    def __str__(self):
        return f"{self.street_name}"
