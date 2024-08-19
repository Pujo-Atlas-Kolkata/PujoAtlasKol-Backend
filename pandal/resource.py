from import_export import resources
from . import models as pandal_models

class PandalResource(resources.ModelResource):
    class Meta:
        model = pandal_models.Pandal