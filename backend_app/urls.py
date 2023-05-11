from django.contrib import admin
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from backend_app import views

app_name = 'backend_app'

urlpatterns = [
 	path('admin/', admin.site.urls),
	path('', views.dashboard, name='dashboard'),
	path('register/', views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
	path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
 	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),
 	
 	path('password_reset/', auth_views.PasswordResetView.as_view(
 		template_name='registration/password_reset.html',
 		email_template_name = 'registration/password_reset_email.html',
 		subject_template_name = 'registration/password_reset_subject.txt',
 		success_url = reverse_lazy('backend_app:password_reset_done')
 		),
 		name='password_reset'),
  	
  	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),
  	
	path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
		template_name='registration/password_reset_confirm.html',
		success_url = reverse_lazy('backend_app:password_reset_complete')
		), 
		name='password_reset_confirm'),
    
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

    
    path('super_user/', views.ListSuperUser.as_view(), name='super_user'),
    path('regular_user/', views.ListRegularUser.as_view(), name='regular_user'),
    path('male/', views.ListMaleUser.as_view(), name='male'),
    path('female/', views.ListFemaleUser.as_view(), name='female'),
   
    

	path('profile/', views.profile, name='profile'),
	path('profile/edit/', views.edit_profile, name='edit_profile'),
	


	path('post/', views.CreatePost.as_view(), name='post'),
	path('list_post/', views.ListPost.as_view(), name='list_post'),
	path('edit_post/<int:pk>/', views.UpdatePost.as_view(), name='edit_post'),
	path('delete_post/<int:pk>/', views.DeletePost.as_view(), name='delete_post'),

  	

  	path('category/', views.CreateCategory.as_view(), name='category'),
	path('list_category/', views.ListCategory.as_view(), name='list_category'),
	path('edit_category/<int:pk>/', views.UpdateCategory.as_view(), name='edit_category'),
	path('delete_category/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),


	path('user/', views.CreateUser.as_view(), name='user'),
	path('list_users/', views.ListUser.as_view(), name='list_user'),
	path('edit_users/<int:pk>/', views.UpdateUser.as_view(), name='edit_user'),
	path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),
	
	

 	
 	






	

	
	
]




