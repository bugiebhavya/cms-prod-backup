from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from modules.users.models import Associate

from django.contrib.auth.models import User 
from modules.users.models import User,UserInterestPercent
from .models import Comment 
from django.forms import inlineformset_factory

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
    download_remain = forms.IntegerField(label=_('Downloads remain'), help_text=_('Number of media User can download'))
    report_access = forms.BooleanField(widget=forms.CheckboxInput, label=_('Report Access'))

class CustomUserCreationForm(UserCreationForm):
    position_held = forms.CharField(required=True, label=_("Position held"))
    associate = forms.ModelChoiceField(queryset=Associate.objects, required=True, label=_("Associate"))
    download_remain = forms.IntegerField(label=_('Downloads remain'), help_text=_('Number of media User can download'))
    report_access = forms.BooleanField(widget=forms.CheckboxInput, label=_('Report Access'))

class UserForm(forms.ModelForm):
	position_held = forms.CharField(required=True, label=_("Position held"))
	associate = forms.ModelChoiceField(queryset=Associate.objects, required=True, label=_("Associate"))
	download_remain = forms.IntegerField(label=_('Downloads remain'), help_text=_('Number of media User can download'))
	class Meta:
		model = User
		exclude = ()
		ordered_field_names = ['username', 'password']
		
UserInterestFormSet = inlineformset_factory(
    User, UserInterestPercent, form=UserForm,
    fields=['interest', 'percent'], extra=1, can_delete=True
    )
