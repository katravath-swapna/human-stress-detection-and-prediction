from django.db import models

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)  # Store hashed password
    cpassword = models.CharField(max_length=100,default='')
    class Meta:
        db_table = 'hello_user'

    def __str__(self):
        return self.username
