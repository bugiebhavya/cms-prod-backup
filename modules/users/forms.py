from django import forms
from .models import Favorite, User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password
import pdb

class FavoriteForm(forms.ModelForm):
	class Meta:
		model = Favorite
		exclude = ('content_type', 'object_id', 'content_object', 'count')


class UserChangePassword(forms.ModelForm):
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=200)
	new_password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=200)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=True, max_length=200)
	
	class Meta:
		model = User
		fields = ('password',)

	def clean(self):
		cleaned_data = super(UserChangePassword, self).clean()
		confirm_password =cleaned_data.get('confirm_password')
		password = cleaned_data.get('password')
		new_password = cleaned_data.get('new_password')
		if new_password != confirm_password:
			raise forms.ValidationError(_("New password & Confirm password does not match."))
		elif not check_password(password, self.instance.password):
			raise forms.ValidationError(_("Incorrect current password."))

	def save(self, commit=True):
		user = super(UserChangePassword, self).save(commit)
		if commit:
			user.set_password(self.cleaned_data.get('confirm_password'))
			user.save()
		return user