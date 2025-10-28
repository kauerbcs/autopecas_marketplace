from django.contrib import admin

from .models import Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'quantity', 'created_at', 'updated_at')
	search_fields = ('name',)
