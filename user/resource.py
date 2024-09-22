from import_export import resources
from . import models as user_models

class UserResource(resources.ModelResource):
    class Meta:
        model = user_models.User