from django.urls import path
from .views import AnimalView, AnimalDetailView, RegisterView, LoginView, AnimarlCreateView


urlpatterns = [
    path('animals/', AnimalView.as_view()),
    path('animal/<pk>', AnimalDetailView.as_view() ),
    path('register/', RegisterView.as_view() ),
    path('login/', LoginView.as_view() ),
    path('createAnimal/' , AnimarlCreateView.as_view())
]
