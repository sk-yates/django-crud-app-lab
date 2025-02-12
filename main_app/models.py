from django.db import models

# Create your models here.

class Quest(models.Model):
    title = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    is_complete = models.BooleanField(default=False)

    # new code below
    def __str__(self):
        return self.title