from django.db import models
from django.contrib.auth.models import User
from .choices import ANIMAL_CHOICE, ANIMAL_GENDER
import uuid
from django.utils.text import slugify

# Create your models here.

class BaseClass(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class Category(BaseClass):
    category_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name

class AnimalBreed(BaseClass):
    animal_breed = models.CharField(max_length=16)
    
    def __str__(self):
        return self.animal_breed
    
class AnimalColor(BaseClass):
    animal_color = models.CharField(max_length=16)
    
    def __str__(self):
        return self.animal_color
    
class Animal(BaseClass):
    animal_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="animal")
    animal_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="animal_category")
    animal_views = models.IntegerField(default=0)
    animal_likes = models.IntegerField(default=1)
    animal_name = models.CharField(max_length=16)
    animal_description = models.TextField()
    animal_slug = models.SlugField(max_length=255, unique=True, blank=True)
    animal_gender = models.CharField(max_length=8, choices=ANIMAL_GENDER)
    animal_breed = models.ManyToManyField(AnimalBreed)
    animal_color = models.ManyToManyField(AnimalColor)
    
    def save(self, *args, **kwargs):
        uid = str(uuid.uuid4()).split('-')
        self.animal_slug = slugify(self.animal_name) + '-' + uid[0]
        super(Animal, self).save(*args, **kwargs)
        
    def incrementView(self):
        self.animal_views += 1
        self.save()
        
    def incrementLikes(self):
        self.animal_likes += 1
        self.save()
    
    def __str__(self):
        return f"{self.animal_name}: Owner: {self.animal_owner}"
    
    class Meta:
        ordering = ['animal_name']
    
class AnimalLocation(BaseClass):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="animal_location")
    location = models.CharField(max_length=50)
    
    def __str__(self):
        return self.location
    
class AnimalImages(BaseClass):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="animal_image")
    animal_image = models.ImageField(upload_to='animal_images/')
    
    def __str__(self):
        return f"{self.animal.animal_name} Image"
    