from import_export import resources
from . import models as transport_models

class MetroResource(resources.ModelResource):
    class Meta:
        model = transport_models.Metro