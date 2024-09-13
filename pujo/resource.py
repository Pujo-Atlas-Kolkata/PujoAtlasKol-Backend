from import_export import resources
from . import models as pujo_models

class PujoResource(resources.ModelResource):
    class Meta:
        model = pujo_models.Pujo