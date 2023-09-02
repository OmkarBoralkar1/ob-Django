from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.contrib.auth.models import User
# from collections.abc import Iterator
class UserManager(BaseUserManager):
    def create_user(self, username1, password=None, email1=None, **extra_fields):
        if not username1:
            raise ValueError("The username must be set")
        email1 = self.normalize_email(email1)
        user = self.model(username1=username1, email1=email1, **extra_fields)
        # user.set_password(password)
        user.save()
        return user
class User1(models.Model):
    user =models.OneToOneField(User ,on_delete=models.CASCADE,  related_name='User1', blank=True, null=True)
    username1 = models.CharField(max_length=100,null=True)
    password1 = models.CharField(max_length=100,null=True)
    email1 = models.EmailField(null=True)
    # user_id=models.EmailField(null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    objects = UserManager()

    def __str__(self):
        return self.username1
class Hotel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    hotel_name = models.TextField(null=True)
    description = models.TextField(null=True)
    price = models.TextField(null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    video = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return  self.hotel_name
class HotelReview(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    review_text = models.TextField(null=True)
    def __str__(self):
        return  self.username
class Reply(models.Model):
    review = models.ForeignKey(HotelReview, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    reply = models.TextField(null=True)

    def __str__(self):
        return self.review.review_text

