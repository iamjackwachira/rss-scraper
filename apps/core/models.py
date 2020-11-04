from django.db import models


class BaseModel(models.Model):
    """
    An abstract base class model that provides self updating
    ``created_on`` and ``modified_on`` fields.
    """

    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
