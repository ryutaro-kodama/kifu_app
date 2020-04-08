from django.contrib import admin

# Register your models here.

from .models import HistoryList, LatestSync

admin.site.register(HistoryList)
admin.site.register(LatestSync)

class LargeclassAdmin(admin.ModelAdmin):
    list_display = ('name')