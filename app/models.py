from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
#to do item
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    due_date = models.DateTimeField("due date")
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.user)

