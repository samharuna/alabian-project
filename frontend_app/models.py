from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Home(models.Model):
	background_img = models.ImageField(verbose_name = 'Background Image', blank=True, null=True)
	name = models.CharField(verbose_name = 'Profile Name', max_length=100, default=None)
	home_desc = models.CharField(verbose_name = 'Home Description', max_length=200)
	
	def __str__(self):
		return self.name



class About(models.Model):
	about_img = models.ImageField(verbose_name = 'Background Image', blank=True, null=True)
	name = models.CharField(verbose_name = 'Full Name', max_length=100, default=None)
	about_desc = models.CharField(verbose_name = 'About Description', max_length=100)
	email = models.EmailField(default=None, max_length=254, blank=False, unique=True,
		        error_messages={'required': 'Please provide your email address.',
		                        'unique': 'An account with this email exist.'},)
	phone_number = models.CharField(verbose_name = 'Mobile Number' , blank=True, null=True, max_length=20)
	about_cont = models.TextField(verbose_name = 'About Content')

# KNOWLEDGE
	HTML5 = models.CharField(verbose_name = 'HTML5' , blank=True, null=True, max_length=3)
	CSS3 = models.CharField(verbose_name = 'CSS3' , blank=True, null=True, max_length=3)
	PYTHON = models.CharField(verbose_name = 'PHYHON' , blank=True, null=True, max_length=3)
	GIT = models.CharField(verbose_name = 'GIT' , blank=True, null=True, max_length=3)

	def __str__(self):
		return self.name



class Qualification(models.Model):
	qualification_title = models.CharField(verbose_name='Qualification Description', max_length=100, default=None)
	qualification_desc = models.TextField(verbose_name='Qualification Content')
	
	def __str__(self):
		return self.qualification_title



class Portfolio(models.Model):
	portfolio_img = models.ImageField(verbose_name = 'Portfolio Image', blank=True, null=True)
	portfolio_title = models.CharField(verbose_name='Portfolio Title', max_length=100)
	portfolio_desc = models.TextField(verbose_name='Portfolio Description')
	last_edited = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.portfolio_title


class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	

class Blog(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	blog_img = models.ImageField(verbose_name = 'Blog Image', blank=True, null=True)
	blog_desc = models.CharField(verbose_name = 'Blog Description', max_length=200)
	author_image = models.ImageField(verbose_name = 'Author Image', blank=True, null=True)
	blog_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Blog Author')
	published_date = models.DateTimeField(blank=True, null=True)
	content = models.TextField(verbose_name='Content', blank=True, null=True)
	
	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.blog_desc


class Banner(models.Model):
	banner_for_blog = models.ImageField(verbose_name = 'Banner Image', blank=True, null=True)
	banner_title = models.CharField(verbose_name = 'Banner Title', max_length=250, default='')
	banner_description = models.CharField(verbose_name = 'Banner Description', max_length=300, default='')
	published_date = models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return str(self.banner_for_blog)



class ContactForm(models.Model):
	name = models.CharField(verbose_name='Name', max_length=150)
	email = models.EmailField()
	subject = models.CharField(verbose_name='Subject', max_length=150)
	message = models.TextField(verbose_name='Message', blank=True, null=True)

	def __str__(self):
		return self.name


class Marquee(models.Model):
	message = models.TextField(verbose_name='Message', blank=True, null=True)

	def __str__(self):
		return self.message