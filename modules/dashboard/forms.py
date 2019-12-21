# from users.models import MembershipStatus
# from django import forms
# from wagtail.users.forms import UserEditForm, UserCreationForm


# def upload_avatar_to(instance, filename):
# 	filename, ext = os.path.splitext(filename)
# 	return os.path.join(
# 		'avatar_images',
# 		'avatar_{uuid}_{filename}{ext}'.format(
# 			uuid=uuid.uuid4(), filename=filename, ext=ext)
#     )
# class CustomUserEditForm(UserEditForm):
#     # country = forms.CharField(required=True, label=_("Country"))
#     # status = forms.ModelChoiceField(queryset=MembershipStatus.objects, required=True, label=_("Status"))
#     avatar = forms.ImageField(verbose_name='Profile picture', upload_to=upload_avatar_to, blank=True,)


# class CustomUserCreationForm(UserCreationForm):
#     avatar = forms.ImageField(verbose_name='Profile picture', upload_to=upload_avatar_to, blank=True,)