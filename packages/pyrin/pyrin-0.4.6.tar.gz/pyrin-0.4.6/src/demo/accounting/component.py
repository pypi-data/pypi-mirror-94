# -*- coding: utf-8 -*-
"""
accounting component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component

from demo.accounting import AccountingPackage
from demo.accounting.manager import AccountingManager


@component(AccountingPackage.COMPONENT_NAME)
class AccountingComponent(Component, AccountingManager):
    """
    accounting component class.
    """
    pass
