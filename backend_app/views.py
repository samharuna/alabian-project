from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm
from backend_app.forms import (RegForm, EditUserForm, PostForm, 
    CategoryForm, AuthenticationForm, UserForm)
from django.contrib.auth import update_session_auth_hash 
from django.contrib import messages
from django.contrib.auth import authenticate
from backend_app.models import Post, Category, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, UpdateView, DeleteView, CreateView)
from django.contrib.auth.models import User
from typing import List
from django.urls import reverse_lazy
from django.db.models import Count

# Create your views here.

@login_required
def dashboard(request):
  post_count = Post.objects.count()
  category_count = Category.objects.count()
  super_user_count = UserProfile.objects.count()
  regular_user_count = UserProfile.objects.count()
  male_count = UserProfile.objects.count()
  female_count = UserProfile.objects.count()

  return render(request, 'backend_app/index.html', {'post_count': post_count, 
    'category_count': category_count, 
    'super_user_count': super_user_count,
    'regular_user_count': regular_user_count,
    'male_count': male_count,
    'female_count': female_count,
    })


class ListSuperUser(ListView):
  model = UserProfile
  template_name = 'backend_app/super_user.html'
  context_object_name = 'super_user'


class ListRegularUser(ListView):
  model = UserProfile
  template_name = 'backend_app/regular_user.html'
  context_object_name = 'regular_user'


class ListMaleUser(ListView):
  model = UserProfile
  template_name = 'backend_app/male.html'
  context_object_name = 'male'


class ListFemaleUser(ListView):
  model = UserProfile
  template_name = 'backend_app/female.html'
  context_object_name = 'female'


@login_required
def user(request):
  if request.method == 'POST':
    add_user= AddUser(request.POST)
    if user.is_valid():
      user.save()
      messages.success(request, 'User added successfully.')
      return redirect('backend_app:user')
  else:
    user = User()
  context = {'user':user}
  return render(request, "backend_app/user.html", context)



@login_required
def logout(request):
    return render(request, 'registration/logout.html')



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('backend_app:index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "registration/login.html",
                    context={"form":form})



def register(request):
    form = RegForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your Registration was done successfully, Click on the Login button below to Login')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        return redirect('backend_app:register')
    else:
        form = RegForm()
    return render(request, 'registration/register.html', {'form': form})



@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, form.user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('backend_app:password_change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/password_change.html', {'form': form})



@login_required
def password_reset(request):
    if request.method == 'POST':
        form = SetPasswordForm(request=request, data=request.POST)
        if form.is_valid():
            messages.success(request, 'Your Password was Reset successfully updated!')
            password1 = form.cleaned_data.get('new_password1')
            password2 = form.cleaned_data.get('new_password2')
            user = set_password(password1=password1, password2=password2)
            if user is not None:
                set_password(request, user)
                return redirect('password_reset')
            else:
                messages.error(request, "password_mismatch")
        else:
            messages.error(request, "password_mismatch")
    form = SetPasswordForm()
    return render(request = request,
                    template_name = "registration/password_reset.html",
                    context={"form":form})


@login_required
def password_reset_confirm(request, uidb64, token):
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context = {}

    if default_token_generator.check_token(user, token):
        context["validlink"] = True
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('backend_app:password_reset_complete')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(user=request.user)
        
    return render(request, "registration/password_reset_confirm.html", {'form': form})



@login_required    
def password_reset_done(request):
  return redirect('backend_app:password_reset_confirm')
  return render(request, "registration/password_reset_done.html")



@login_required    
def password_reset_complete(request):
  return render(request, "registration/password_reset_complete.html")


@login_required  
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile was successfully updated!')
            return redirect('backend_app:profile')
    else:
        form = EditUserForm(instance=request.user)
        context = {'form': form}
        return render(request, 'backend_app/edit_profile.html', context)

def profile(request):
    args = {'user': request.user}
    return render(request, 'backend_app/profile.html', args)



class CreatePost(CreateView):
  model = Post
  form_class = PostForm
  template_name = 'backend_app/post.html'
  success_url = reverse_lazy('backend_app:list_post')

class ListPost(ListView):
  model = Post
  template_name = 'backend_app/list_post.html'
  context_object_name = 'list_post'

class UpdatePost(UpdateView):
  model = Post
  form_class = PostForm
  template_name = 'backend_app/edit_post.html'
  success_url = reverse_lazy('backend_app:list_post')

class DeletePost(DeleteView):
  model = Post
  template_name = 'backend_app/delete_post.html'
  success_url = reverse_lazy('backend_app:list_post')




class CreateCategory(CreateView):
  model = Category
  form_class = CategoryForm
  template_name = 'backend_app/category.html'
  success_url = reverse_lazy('backend_app:list_category')

class ListCategory(ListView):
  model = Category
  template_name = 'backend_app/list_category.html'
  context_object_name = 'list_category'

class UpdateCategory(UpdateView):
  model = Category
  form_class = CategoryForm
  template_name = 'backend_app/edit_category.html'
  success_url = reverse_lazy('backend_app:list_category')

class DeleteCategory(DeleteView):
  model = Category
  template_name = 'backend_app/delete_category.html'
  success_url = reverse_lazy('backend_app:list_category')



class CreateUser(CreateView):
  model = UserProfile
  form_class = UserForm
  template_name = 'backend_app/user.html'
  success_url = reverse_lazy('backend_app:user')

class ListUser(ListView):
  model = UserProfile
  template_name = 'backend_app/list_user.html'
  context_object_name = 'list_user'

class UpdateUser(UpdateView):
  model = UserProfile
  form_class = UserForm
  template_name = 'backend_app/edit_user.html'
  success_url = reverse_lazy('backend_app:list_user')

class DeleteUser(DeleteView):
  model = UserProfile
  template_name = 'backend_app/delete_user.html'
  success_url = reverse_lazy('backend_app:list_user')