from dataclasses import field, fields
import email
from ipaddress import collapse_addresses
from os import popen
from pyexpat import model
from statistics import mode
from turtle import title
from unittest.util import _MAX_LENGTH
from wsgiref import validate
from rest_framework import serializers
#from myproj.testapp.models import BlogPost
from testapp.models import Contact, BlogPost
from django import forms

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        #fields = ['name', 'email', 'phone', 'title']

class ContactForm(forms.ModelForm):
    class Meta: 
        model = Contact
        fields = '__all__'

class ContactSerializerOne(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    email = serializers.EmailField(max_length = 100)
    phone = serializers.CharField(max_length = 100)
    title = serializers.CharField(max_length = 100)

    def create(self, validated_data):
        return Contact(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        #fields = '__all__'
        exclude = ['user', 'is_active']

class PostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'