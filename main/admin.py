from django.contrib import admin
from .models import Info, Answer
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin

class InfoAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Info, InfoAdmin)
admin.site.register(Answer)
