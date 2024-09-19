from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = "__all__"
        fields = ['category_name']

class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        # fields = "__all__"
        fields = ['animal_breed']

class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalColor
        # fields = "__all__"
        fields = ['animal_color']

class AnimalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImages
        # fields = "__all__"
        fields = ['animal_image']
        
class AnimalSerializer(serializers.ModelSerializer):
    # method to view all the field in JSON response
    # animal_category = CategorySerializer()
    
    #method2 to view only spcific response in JSON
    animal_category = serializers.SerializerMethodField()
    
    def get_animal_category(self, obj):
        return obj.animal_category.category_name
    
    animal_breed = AnimalBreedSerializer(many=True)
    animal_color = AnimalColorSerializer(many=True)
    # animal_breed = serializers.SerializerMethodField()
    # def get_animal_breed(self, obj):
    #     return [breed.animal_breed for breed in obj.animal_breed.all()]
    
    # animal_color = serializers.SerializerMethodField()
    # def get_animal_color(self, obj):
    #     return [color.animal_color for color in obj.animal_color.all()]
    
    # enable one of two method of image after debugging
    # use different var name than model's related_name, then give source of related_name
    # images = AnimalImagesSerializer(source = "animal_image", many=True) 
    
    # user the same var name as related_name and no need to use 'source' parameter
    # animal_image = AnimalImagesSerializer(many=True) 
    
    # method3 to view custom data only
    # def to_representation(self, instance):
    #     animal_color_serializer = AnimalColorSerializer(instance.animal_color.all(), many=True)
        
    #     payload = {
    #         'animal_views' : instance.animal_views,
    #         'animal_likes' : instance.animal_likes,
    #         'animal_name' : instance.animal_name,
    #         'animal_description' : instance.animal_description,
    #         'animal_color' : animal_color_serializer.data
    #     }
    #     return payload
    
        
    def create(self, data):
        animal_breed = data.pop('animal_breed')
        animal_color = data.pop('animal_color')
       
        animal = Animal.objects.create(animal_category=Category.objects.get(category_name="birds"), **data)
        
        for ab in animal_breed:
            animal_breed_obj = AnimalBreed.objects.get(animal_breed=ab['animal_breed'])
            animal.animal_breed.add(animal_breed_obj)
            
        for color in animal_color:
            val = AnimalColor.objects.get(animal_color=color['animal_color'])
            animal.animal_color.add(val)
            
        return animal
    
    def update(self, instance, data):
        if 'animal_breed' in data:
            animal_breed = data.pop('animal_breed')
            instance.animal_breed.clear()
            for breed in animal_breed:
                val = AnimalBreed.objects.get(animal_breed=breed["animal_breed"])
                instance.animal_breed.add(val)
                
        if 'animal_color' in data:    
            animal_color = data.pop('animal_color')
            instance.animal_color.clear()
            for color in animal_color:
                val = AnimalColor.objects.get(animal_color=color["animal_color"])
                instance.animal_color.add(val)
        
        instance.animal_name = data.get('animal_name', instance.animal_name)
        instance.animal_description = data.get('animal_description', instance.animal_description)
        instance.animal_gender = data.get('animal_gender', instance.animal_gender)
        instance.animal_owner = data.get('animal_owner', instance.animal_owner)
        instance.save()
        return instance

    class Meta:
        model = Animal
        exclude = ['updated_at']
        
        

class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocation
        fields = "__all__"


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        if 'username' in data:
            user = User.objects.filter(username = data['username'])
            if user.exists():
                raise serializers.ValidationError("Username is alreadu taken")
            
        if 'email' in data:
            email = User.objects.filter(email = data['email'])
            if email.exists():
                raise serializers.ValidationError("Email is already taken")
            
        return data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        if 'username' in data:
            username = User.objects.filter(username = data['username'])
            if not username.exists():
                raise serializers.ValidationError('Username doesn\'t exist')
                
        return data