from django.urls import path
from frontend_app import views


app_name = 'frontend_app'

urlpatterns = [
	path('', views.blog, name='blog'),
	path('contact/', views.contact, name='contact'),
	path('blog_detail/<int:blog_id>', views.blog_detail, name='blog_detail'),
]