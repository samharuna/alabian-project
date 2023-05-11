from django.contrib import admin
from backend_app.models import Post, Category, UserProfile

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}



admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)