from import_export import resources
from . import models as review_models

# Create your tests here.
class ReviewResource(resources.ModelResource):
    class Meta:
        model = review_models.Review