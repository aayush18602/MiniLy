from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class shorturl(models.Model):
    original_link = models.URLField(blank=False)
    short_name = models.CharField(max_length=15,blank=False)
    visit_no = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_name} - {self.user}"
    