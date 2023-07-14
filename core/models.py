from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class item(models.Model):
    iid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    price = models.IntegerField(null=True, blank=True)
    image = models.FileField(upload_to="images/")

    def __str__(self) -> str:
        return self.title

class UserCreation(models.Model):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100,  null=False)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=18)
    dob = models.DateField(null=True, blank=True)  # Add the dob field

    def create(self):
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        user.save()
        return user.id

    def __str__(self):
        return self.username