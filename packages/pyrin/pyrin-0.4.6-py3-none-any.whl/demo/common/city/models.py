# -*- coding: utf-8 -*-
"""
city models module.
"""

from sqlalchemy import Unicode, Integer, ForeignKey, CheckConstraint

from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.utils.sqlalchemy import check_constraint


class CityBaseEntity(CoreEntity):
    """
    city base entity class.
    """

    _table = 'city'

    id = CoreColumn(name='id', autoincrement=True, type_=Integer, primary_key=True)


class CityEntity(CityBaseEntity):
    """
    city entity class.
    """

    _extend_existing = True

    @classmethod
    def _customize_table_args(cls, table_args):
        """
        customizes different table args for current entity type.

        this method is intended to be overridden by subclasses to customize
        table args per entity type if the required customization needs extra work.
        it must modify input dict values in-place if required.
        if other table args must be added (ex. UniqueConstraint or CheckConstraint ...)
        it must return those as a tuple. it could also return a single object as
        extra table arg (ex. a single UniqueConstraint).
        if no changes are required this method should not return anything.

        :param dict table_args: a dict containing different table args.
                                any changes to this dict must be done in-place.

        :rtype: tuple | object
        """

        return CheckConstraint(cls.name.notin_(['ali', 'reza']))
        # return check_constraint('name', ['ali', 'reza'], use_in=False)

    name = CoreColumn(name='name', type_=Unicode)

    province_id = CoreColumn(ForeignKey('province.id'),
                             name='province_id', type_=Integer)


class MyEntity(CoreEntity):
    """
    city base entity class.
    """

    _table = 'my_entity_table'

    id = CoreColumn(name='id', autoincrement=True, type_=Integer, primary_key=True)
    name = CoreColumn(name='name', type_=Unicode)
    level = CoreColumn(name='level', type_=Unicode)
