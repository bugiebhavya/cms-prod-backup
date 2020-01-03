from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from modules.users.models import Associate

from django.contrib.auth.models import User 
from .models import Comment 

class AdminLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', 'password',)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('body',)
		widgets = {
			'body': forms.Textarea(attrs={'rows': '1', 'class': 'comment-field', 'placeholder': 'commenting publicly'})
		}




class CustomUserEditForm(UserEditForm):
    position_held = forms.CharField(required=True, label=_("Position held"))
    associate = forms.ModelChoiceField(queryset=Associate.objects, required=True, label=_("Associate"))


class CustomUserCreationForm(UserCreationForm):
    position_held = forms.CharField(required=True, label=_("Position held"))
    associate = forms.ModelChoiceField(queryset=Associate.objects, required=True, label=_("Associate"))