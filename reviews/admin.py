from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from . import models as review_models
from . import resource as review_resource
# Register your models here.
class ReviewAdmin(ImportExportModelAdmin):
    resource_class = review_resource.ReviewResource
    list_display = [field.name for field in review_models.Review._meta.fields]

admin.site.register(review_models.Review, ReviewAdmin)