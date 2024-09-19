from django.shortcuts import render
from django.http import request
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Animal)
from .serializers import (AnimalSerializer, RegisterSerializer, LoginSerializer)
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permission import IsValidUserPermision
# Create your views here.
def welcome(request):
    return render(request, "api/home.html", {"data": "welcome dvs"})

class AnimalDetailView(APIView):
    #import IsAuthenticated from rf.permissions
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk)
            animal.incrementView()
            serializer = AnimalSerializer(animal)
            return Response({
                'status': True,
                'message': 'Fetched using GET',
                'data' : serializer.data
            })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'Something went wrong',
                'data' : {}
            })
            
            
class AnimalView(APIView):
    def get(self, request):
        obj = Animal.objects.all()
        if request.GET.get('search'):
            search = request.GET.get('search')
            obj = obj.filter(
                Q(animal_name__icontains = search) | 
                Q(animal_description__icontains = search) |
                Q(animal_color__animal_color__icontains = search) | 
                Q(animal_gender__iexact = search) 
            )
            # return Response
            
        serializer = AnimalSerializer(obj, many=True)
        return Response({
            'status': True,
            'message': 'Fetched using GET',
            'data' : serializer.data
        })
        
    def post(self, request):
        return Response({
            'status': True,
            'message': 'Fetched using POST',
        })
        
    def put(self, request):
        return Response({
            'status': True,
            'message': 'Fetched using PUT',
        })
        
    def patch(self, request):
        return Response({
            'status': True,
            'message': 'Fetched using PATCH',
        })
    
    def delete(self, request):
        return Response({
            'status' : True,
            'message': 'Feth using DELETE'
        })
        
class RegisterView(APIView):
    def post(self, request):
        try:
            # data = request.data
            serializer = RegisterSerializer(data = request.data)
            if serializer.is_valid():
                
                user = User.objects.create(
                    username = serializer.data['username'],
                    email = serializer.data['email']
                )
                user.set_password(serializer.data['password'])
                user.save()
                
                return Response({
                    'status' : True,
                    'message': 'Account Created',
                    'data': {}
                })
                
            return Response({
                'status' : False,
                'message': 'Key errors',
                'data' : serializer.errors
            })
        
        except Exception as e:
            print(e)
            
            
class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
                if user:
                    token, _ = Token.objects.get_or_create(user = user)
                    return Response({
                        'status': True,
                        'message': 'Login successful',
                        'data': {
                            'token': str(token),
                        }
                    })
                
                return Response({
                    'status' : False,
                    'message' : 'Password is incorrect',
                    'data' : {}
                })
                
            return Response({
                'status' : False,
                'message' : 'keys error',
                'data' : serializer.errors
            })
        
        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message' : 'somethig went wrong',
                'data' : {}
            })
            
            
class AnimarlCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsValidUserPermision]
    def post(self, request):
        try:
            # print(request.data)
            request.data['animal_owner'] = request.user.id
            # print(request.data)
            serializer = AnimalSerializer(data = request.data)
        
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message' : "Animal created successfully",
                    'data' : serializer.data
                })
                
            return Response({
                'status' : False,
                'message' : 'invalid data',
                'data' : serializer.errors
            })
            
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : f'Something went wrong: {str(e)}',
                'data' : {}
            })
            
    def patch(self, request):
        try:
            data = request.data
            if data.get('id') is None:
                return Response({
                    'status' : False,
                    'message' : 'animal id is required',
                    'data' : {}
                })
                
            animal_obj = Animal.objects.filter(uuid=data.get('id'))
            if not animal_obj.exists():
                return Response({
                    'status' : False,
                    'message' : 'animal id is not valid',
                    'data' : {}
                })
            
            animal_obj = animal_obj[0]
            self.check_object_permissions(request, animal_obj) #check whether user has a permission to update object or not - permission.py
            data['animal_owner'] = request.user.id
            serializer = AnimalSerializer(animal_obj, data = request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message' : "Animal updated successfully",
                    'data' : serializer.data
                })
                
            return Response({
                'status' : False,
                'message' : 'invalid data',
                'data' : serializer.errors
            })
                
                    
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : f'something wrong: {str(e)}',
                'data' : {}
            })