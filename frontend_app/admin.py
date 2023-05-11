from django.contrib import admin
from frontend_app.models import Home, About, Banner, Qualification, Portfolio, Blog, ContactForm, Category, Marquee

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}


admin.site.register(Home)
admin.site.register(About)
admin.site.register(Qualification)
admin.site.register(Portfolio)
admin.site.register(Blog)
admin.site.register(Banner)
admin.site.register(Marquee)
admin.site.register(ContactForm)
admin.site.register(Category, CategoryAdmin)


