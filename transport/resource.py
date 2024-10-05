from import_export import resources
from . import models as transport_models

class TransportResource(resources.ModelResource):
    class Meta:
        model = transport_models.Transport