from import_export.admin import ImportExportModelAdmin
from django.contrib import admin 
from . import resource as pandal_resource  
from . import models as pandal_models

class PandalAdmin(ImportExportModelAdmin):
    resource_class = pandal_resource.PandalResource
    list_display = ['name', 'zone']

admin.site.register(pandal_models.Pandal, PandalAdmin)