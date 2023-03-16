import imp
from django.urls import path
from testapp import views
from .views import *

urlpatterns = [
    path('first/', firstAPI),
    path('registration/',  registration),
    path('contact/', ContactAPIView.as_view()),
    path('post/', PostCreateAPIView.as_view()),
    path('post/<int:id>/', PostRetrieveAPIView.as_view()),
    #path('post/<int:id>/', PostUpdateAPIView.as_view()),
    #path('post/<int:id>/', PostDeleteAPIView.as_view())
]