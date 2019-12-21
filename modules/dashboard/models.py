# from django.db import models
# import os, uuid
# # Create your models here.
# from wagtail.contrib.settings.models import BaseSetting, register_setting
# from django.contrib.auth.models import AbstractUser



# def upload_avatar_to(instance, filename):
#     filename, ext = os.path.splitext(filename)
#     return os.path.join(
#         'avatar_images',
#         'avatar_{uuid}_{filename}{ext}'.format(
#             uuid=uuid.uuid4(), filename=filename, ext=ext)
#     )

# class Customer(AbstractUser):
# 	@classmethod
# 	def for_site(cls, site):
# 		print(site)
# 		return site

# 	class Meta:
# 		verbose_name="Customer"
# 	avatar = models.ImageField(
# 		verbose_name='Profile picture',
# 		upload_to=upload_avatar_to,
# 		blank=True,
# 	)

# 	def __str__(self):
# 		return self.username




