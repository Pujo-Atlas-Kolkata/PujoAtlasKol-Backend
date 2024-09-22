from import_export.admin import ImportExportModelAdmin
from django.contrib import admin 
from . import resource as user_resource  
from . import models as user_models

class UserAdmin(ImportExportModelAdmin):
    resource_class = user_resource.UserResource
    list_display =  [field.name for field in user_models.User._meta.fields]

admin.site.register(user_models.User, UserAdmin)
