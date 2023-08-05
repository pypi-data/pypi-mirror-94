# -*- coding: utf-8 -*-
"""
accounting models module.
"""

from sqlalchemy import Unicode, Integer, ForeignKey, CheckConstraint

from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.types.custom import GUID


class AccountEntity(CoreEntity):

    _table = 'account'

    id = CoreColumn(name='account', type_=GUID, primary_key=True)
    owner = CoreColumn(name='owner', type_=Unicode)
