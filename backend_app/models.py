from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.


class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter(sex='M')

class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter(sex='F')

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True)
	email = models.EmailField(max_length=250, default='', unique=True)
	password = forms.CharField(widget=forms.PasswordInput)
	password_again = forms.CharField(widget=forms.PasswordInput)
	first_name = models.CharField(max_length=100, default='')
	last_name = models.CharField(max_length=100, default='')
	image = models.ImageField(upload_to='uploads/profile_image', blank=True)
	sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
	role = models.CharField(max_length=1, choices=[('S', _('Super')), ('R', _('Regular'))])
	active = models.BooleanField(default=True)
	
	
	def __str__(self):
		return self.user.username


class Category(models.Model):
	name = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name


class Post(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	post_title = models.CharField(verbose_name='Post Title', max_length=50)
	content = models.TextField(verbose_name='Content', blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
	post_img = models.ImageField(blank=True, null=True, upload_to='uploads/post_img', verbose_name='Post Image')
	published_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
	
	

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.post_title