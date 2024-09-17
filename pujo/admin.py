from import_export.admin import ImportExportModelAdmin
from django.contrib import admin 
from . import resource as pujo_resource  
from . import models as pujo_models

class PujoAdmin(ImportExportModelAdmin):
    resource_class = pujo_resource.PujoResource
    list_display = ['uuid', 'name', 'city', 'address', 'lat','lon','zone']

admin.site.register(pujo_models.Pujo, PujoAdmin)