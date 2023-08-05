# -*- coding: utf-8 -*-
"""
accounting api module.
"""

import pyrin.utils.unique_id as uuid_utils
from demo.accounting.schema import AccountSchema

from pyrin.api.router.decorators import api
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.core.globals import SECURE_TRUE

import demo.accounting.services as accounting_services

from demo.accounting.models import AccountEntity


# Usage:
# you could implement different api functions here and call corresponding service method this way:
# return accounting_services.method_name(*arg, **kwargs)
from pyrin.database.services import get_current_store


@api('/accounts', methods=HTTPMethodEnum.POST, authenticated=False)
def create(owner=None):
    # uuid = uuid_utils.generate_uuid4()
    # entity = AccountEntity(id=uuid, owner=owner, populate_all=SECURE_TRUE)
    # return entity.save()
    return 1


@api('/accounts', methods=HTTPMethodEnum.GET, authenticated=False, result_schema=AccountSchema())
def get_all():
    store = get_current_store()
    return store.query(AccountEntity.id, AccountEntity.owner).all()


@api('/accounts/<uuid:uuid>', methods=HTTPMethodEnum.GET, authenticated=False)
def get(uuid):
    store = get_current_store()
    return store.query(AccountEntity).filter(AccountEntity.id == uuid).all()
