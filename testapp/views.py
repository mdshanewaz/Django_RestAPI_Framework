from email import header
from gettext import install
from operator import contains
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from testapp.models import Contact
from testapp.serializers import ContactSerializer
from django.shortcuts import render
from .serializers import *
from .models import BlogPost
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status    

# Create your views here.


def homeview(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def firstAPI(request):
    if request.method == "POST":
        name = request.data['name']
        age = request.data['age']
        print(name, age)
        return Response({"name":name, "age": age})

    context = {
        'name' : "Shah Newaz",
        'Institute' : "NSTU",
    }
    return Response(context)

@api_view(['POST',])
def registration(request):
    if request.method == "POST":
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        username = request.data['username']
        email = request.data['email']
        password1 = request.data['password1']
        password2 = request.data['password2']

        if User.objects.filter(username = username).exists():
            return Response({"Error" : "An user with this username is already exists!"})
        elif User.objects.filter(email = email).exists():
            return Response({"Error" : "An user with this email is already exists!"})
        elif password1 != password2:
            return Response({"Error" : "Passwords did not matched!"})
        
        user = User()
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.is_active = True
        
        user.set_password(raw_password=password1)
        user.save()

        return Response({"Success" : "User successfully created"})

class ContactAPIView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request, format = None):

        serializier = ContactSerializerOne(data = request.data)
        if serializier.is_valid():
            serializier.save()

        return Response(serializier.data)

    def put(self, request, format = None):
        contact = Contact.objects.get(id=11)
        serializier = ContactSerializerOne(data = request.data, instance=contact)
        if serializier.is_valid():
           obj =  serializier.save()

        return Response(serializier.data)    
    
    def get(self, request, format = None):
        queryset = Contact.objects.get(id=11)
        serializer = ContactSerializerOne(queryset, many = False)
        return Response(serializer.data)

class PostCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        serializer = PostDetailsSerializer(instance = instance, many = False)

        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = PostDetailsSerializer(queryset, many = True)
        
        return Response(serializer.data)
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_active = True)

        return queryset

class PostRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.filter(is_active = True)
    serializer_class = PostSerializer
    lookup_field = 'id'

    def retrieve(self, request, id, *args, **kwargs):
        instance = BlogPost.objects.get(id = id)
        #queryset = BlogPostComment.objects.filter(BlogPost = instance)
        serializer = PostDetailsSerializer(instance)

        return Response(serializer.data)    

class PostUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.filter(is_active = True)
    serializer_class = PostSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailsSerializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        return serializer.save(user = self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data = request.data, partial = partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        serializer = PostDetailsSerializer(isinstance)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

# class PostDeleteAPIView(DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = BlogPost.objects.filter(is_active=True)
#     serializer_class =  PostSerializer
#     lookup_field = 'id'