from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class House(models.Model):
    # tags, price, location, phonenumber, email, 
    description = models.CharField(max_length=200)
    main_picture = models.ImageField(upload_to='houses-pictures', blank=True)
    tags = TaggableManager()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    location = models.CharField(max_length=200, blank=True)
    phonenumber = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    available = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses_house')

    def get_absolute_url(self):
        return reverse('houses:house_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='houses_comments')
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='comments')

