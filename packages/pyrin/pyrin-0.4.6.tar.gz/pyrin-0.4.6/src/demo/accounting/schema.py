from datetime import datetime

from demo.accounting.models import AccountEntity
from pyrin.api.schema.structs import ResultSchema
from pyrin.core.globals import SECURE_TRUE

i = []

class AccountSchema(ResultSchema):

    default_columns = ['owner']
    default_rename = dict(owner='Owner')

    def get_computed_row_columns(self, row, **options):
        """
        gets a dict containing all computed columns to be added to the result.

        this method is intended to be overridden in subclasses.

        :param ROW_RESULT row: the actual row result to be processed.

        :rtype: dict
        """

        if len(i) < 4:
            i.append(1)
            return dict(sum=1000,
                        date=datetime.now(),
                        entity=AccountEntity(id='my', owner='alireza', populate_all=SECURE_TRUE),
                        row=row,
                        formatted_id='ID: {id}'.format(id=row.id))

        return None

    def get_computed_entity_columns(self, entity, **options):
        """
        gets a dict containing all computed columns to be added to the result.

        this method is intended to be overridden in subclasses.

        :param BaseEntity entity: the actual entity to be processed.

        :rtype: dict
        """

        if len(i) < 4:
            i.append(1)
            return dict(sum=1000,
                        date=datetime.now(),
                        entity=AccountEntity(id='my', owner='alireza', populate_all=SECURE_TRUE),
                        formatted_id='ID: {id}'.format(id=entity.id))

        return None
