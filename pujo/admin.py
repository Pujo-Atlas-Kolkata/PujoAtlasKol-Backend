from import_export.admin import ImportExportModelAdmin
from django.contrib import admin 
from . import resource as pujo_resource  
from . import models as pujo_models

class PujoAdmin(ImportExportModelAdmin):
    resource_class = pujo_resource.PujoResource
    list_display = [field.name for field in pujo_models.Pujo._meta.fields]

admin.site.register(pujo_models.Pujo, PujoAdmin)