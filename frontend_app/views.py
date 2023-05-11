from django.shortcuts import render, redirect
from django.template.loader import get_template 
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from frontend_app.models import Home, About, Qualification, Portfolio, Blog, ContactForm, Banner, Marquee
from frontend_app.forms import ContactForm
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.

def index(request):
	show_home = Home.objects.all()
	show_about = About.objects.all()
	show_qualification = Qualification.objects.all()
	show_portfolio = Portfolio.objects.all()
	
	
	index_dict = {
		'home_list':show_home,
		'about_list':show_about,
		'qualification_list':show_qualification,
		'portfolio_list':show_portfolio,

	}
	return render(request, 'frontend_app/index.html', context=index_dict)



def blog(request):
	show_banner = Banner.objects.all()
	show_blog = Blog.objects.all()
	show_marquee = Marquee.objects.all()
	latest = Blog.objects.order_by('-last_edited')[0:3]

	blog_dict = {
		'banner_list':show_banner,
		'blog_list':show_blog,
		'marquee_list':show_marquee,
		'latest':latest
	}
	return render(request, 'frontend_app/blog.html', context=blog_dict)


def blog_detail(request, blog_id):
	blog_detail = Blog.objects.get(pk=blog_id)
	return render(request, 'frontend_app/blog_detail.html', {'blog_det':blog_detail})


	search_term=''
	if 'search' in request.GET:
		search_term = request.GET['search']
		blog_detail = blog_detail.filter(text__icontains="")
	
	return render(request, 'frontend_app/blog_detail.html', {'search_term':search_term})



	

def contact(request):
	Contact_Form = ContactForm
	if request.method == 'POST':
		form = Contact_Form(data=request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'We have received your message and would like to thank you for writing to us. If your inquiry is urgent, please use the telephone number listed below to talk to one of our staff members. Otherwise, we will reply by email as soon as possible.')
			name = request.POST.get('name')
			email = request.POST.get('email')
			subject = request.POST.get('subject')
			message = request.POST.get('message')

			template = get_template('frontend_app/contact.txt')
			context = {
				'name' : name,
				'email' : email,
				'subject' : subject,
				'message' : message,
			}
			
			content = template.render(context)
			email = EmailMultiAlternatives(
				'New message from Python Project',
				content,
				'Code with Sam' + '',
				['mrsaharuna@gmail.com'],
			headers = { 'Reply To': email }
			)

		email.send()
		return redirect('frontend_app:contact')

	else:
		form = ContactForm()
	return render(request, 'frontend_app/contact.html', { 'form':Contact_Form })
