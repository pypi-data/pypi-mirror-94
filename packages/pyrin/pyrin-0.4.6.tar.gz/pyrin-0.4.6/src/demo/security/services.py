# -*- coding: utf-8 -*-
"""
security services module.
"""

from pyrin.application.services import get_component

from demo.security import SecurityPackage


def login(username, password, **options):
    """
    logs in the provided user and gets a valid token.

    :param str username: username.
    :param str password: password.

    :raises InvalidUserInfoError: invalid user info error.
    :raises UserNotFoundError: user not found error.
    :raises UserIsNotActiveError: user is not active error.

    :returns: a valid token.
    :rtype: str
    """

    return get_component(SecurityPackage.COMPONENT_NAME).login(username, password, **options)


import pyrin.security.services as security_services

security_services.has_permission(1, [2])
security_services.has_permission(1, [2])
security_services.has_permission(1, [2])
security_services.has_permission(1, [2])
