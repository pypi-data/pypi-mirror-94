from typing import List
from typing import Type

from django.db import models


def get_update_fields(cls: Type[models.Model]) -> List[str]:
    """Return list of names of model fields that can be updated excluding unique_fields"""

    def _should_be_updated(field):
        return (
            not (field.many_to_many or field.one_to_many)
            and not field.auto_created
        )

    return [
        field.name for field in cls._meta.get_fields()
        if _should_be_updated(field)
    ]
