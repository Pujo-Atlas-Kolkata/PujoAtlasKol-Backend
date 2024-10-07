from import_export.admin import ImportExportModelAdmin
from django.contrib import admin 
from . import resource as transport_resource  
from . import models as transport_models

class MetroAdmin(ImportExportModelAdmin):
    resource_class = transport_resource.MetroResource
    list_display = [field.name for field in transport_models.Metro._meta.fields]

admin.site.register(transport_models.Metro, MetroAdmin)