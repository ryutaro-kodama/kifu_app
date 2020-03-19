from django.contrib import admin

# Register your models here.

from .models import HistoryList

admin.site.register(HistoryList)

class LargeclassAdmin(admin.ModelAdmin):
    list_display = ('name')