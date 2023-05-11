from django import forms
from frontend_app.models import ContactForm
 

class ContactForm(forms.ModelForm):
     class Meta():
          model = ContactForm
          fields = ('name', 'email', 'subject', 'message')
          widgets = {
               'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your Full Name', 'size':70}),
               'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email', 'size':70}),
               'subject': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your Subject', 'size':70}),
               'message' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Type your Message Here', 'size':70}),

          }
