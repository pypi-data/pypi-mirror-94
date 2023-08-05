# -*- coding: utf-8 -*-
"""
accounting exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AccountingException(CoreException):
    """
    accounting exception.
    """
    pass


class AccountingBusinessException(CoreBusinessException, AccountingException):
    """
    accounting business exception.
    """
    pass
