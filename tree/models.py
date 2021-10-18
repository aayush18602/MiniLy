from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tree(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    original_link = models.URLField(blank=False)
    short_name = models.CharField(max_length=30,blank=False)
    cr_date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return f"{self.short_name} - {self.user}"
    