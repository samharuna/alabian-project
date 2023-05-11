from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from backend_app.models import Post, Category, UserProfile
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth import (
    authenticate, get_user_model, password_validation)


class SetPasswordForm(forms.Form):
  
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    new_password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user



class AuthenticationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class RegForm(UserCreationForm):
	class Meta():
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

def clean_email(self):
    email = self.cleaned_data.get('email')
    qs = User.objects.filter(email=email)
    if qs.exists():
        raise forms.ValidationError("email is taken")
    return email

def clean_password2(self):
    # Check that the two password entries match
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError("Passwords don't match")
    return password2


class EditUserForm(UserChangeForm):
	class Meta():
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')


class PostForm(forms.ModelForm):
	class Meta():
		model = Post
		fields = ('post_title', 'author', 'category', 'post_img', 'content')


class CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = ('name', 'slug')
    


class UserForm(forms.ModelForm):
    GENDER_CHOICE = [
    ('select your gender', 'Select Your Gender'),
    ('male', 'Male'),
    ('female', 'Female'),
    ]

    ROLE = [
    ('select your role', 'Select Your Role'),
    ('super user', 'Super User'),
    ('regular user', 'Regular User'),
   
    ]
    email = forms.EmailField(disabled=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    gender = forms.CharField(required=False, 
                    widget=forms.Select(attrs={'class':'form-control'}, choices=GENDER_CHOICE))
    role = forms.CharField(required=False, 
                    widget=forms.Select(attrs={'class':'form-control'}, choices=ROLE))

    class Meta():
        model = UserProfile
        fields = ('user', 'first_name', 'last_name', 'image')





class PasswordReset(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )




class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')




class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator




class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    # def get_context_data(self, **kwargs):
    #     context = super(PasswordResetCompleteView, self).get_context_data(**kwargs)
    #     context['login_url'] = resolve_url(settings.LOGIN_URL)
    #     return context


