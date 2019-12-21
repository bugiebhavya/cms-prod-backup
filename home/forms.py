from django import forms
from django.contrib.auth.models import User 
from .models import Comment 

class AdminLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', 'password',)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')