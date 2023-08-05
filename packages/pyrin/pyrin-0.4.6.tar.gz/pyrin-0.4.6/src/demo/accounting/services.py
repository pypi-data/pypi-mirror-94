# -*- coding: utf-8 -*-
"""
accounting services module.
"""

from pyrin.application.services import get_component

from demo.accounting import AccountingPackage


# Usage:
# you could implement different services here and call corresponding manager method this way:
# return get_component(AccountingPackage.COMPONENT_NAME).method_name(*arg, **kwargs)
