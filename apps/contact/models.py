from django.db import models

from common.models import BaseModel


class Contact(BaseModel):
    gmail=models.EmailField(max_length=50)
    fullname=models.CharField(max_length=50)
    message=models.CharField(max_length=1000)

    class Meta:
        db_table = 'Contact'

    def __str__(self):
        return self.gmail