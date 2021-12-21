from django.conf import settings
from django.db import models
from django.db.models import Model
from django.urls import reverse
# Create your models here.
from accounts.models import User
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,db_constraint=False)
    title = models.CharField(max_length = 50,verbose_name = "Title")
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True,)
    slug = models.SlugField(unique=True, max_length=100)


    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_date']

