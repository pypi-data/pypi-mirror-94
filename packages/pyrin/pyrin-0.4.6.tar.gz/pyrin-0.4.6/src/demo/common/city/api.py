# -*- coding: utf-8 -*-
"""
city api module.
"""

import time

from flask import url_for

import pyrin.globalization.datetime.services as datetime_services

from pyrin.api.router.decorators import api
from pyrin.caching.decorators import cached
from pyrin.caching.remote.decorators import memcached
from pyrin.core.enumerations import HTTPMethodEnum

import pyrin.processor.cors.services as cors_services
import demo.common.city.services as city_services
from pyrin.core.exceptions import CoreException
from pyrin.core.structs import DTO
from pyrin.security.session.services import get_current_request

#
# @api('/car/<slug>', authenticated=False)
# def test1(**options):
#     return 'test1'
#
#
# @api('/car/comments', authenticated=False, methods=HTTPMethodEnum.GET)
# def test2(**options):
#     preflight = cors_services.get_preflight_headers(['get', 'post'])
#     actual = cors_services.get_actual_headers()
#     actual.update(preflight)
#     return 'test2', actual
#
#
# @api('/cities/<int:city_id>', methods=HTTPMethodEnum.GET, authenticated=False)
# def get(city_id, **options):
#     """
#     gets the specified city.
#
#     :param int city_id: city id to get its info.
#
#     :raises CityNotFoundError: city not found error.
#
#     :returns: dict(int id,
#                    str name,
#                    int province_id: province id)
#
#     :rtype: dict
#     """
#
#     return city_services.get(city_id, **options)
#
#
# @api('/cities', methods=HTTPMethodEnum.DELETE, authenticated=False)
# def clear(**options):
#     return city_services.clear()
#
#
# @api('/cities', methods=HTTPMethodEnum.GET,
#      authenticated=False, no_cache=True, paged=True, indexed=True)
# def find(name, age, *, gender, level=None, **filters):
#     """
#     finds cities with given filters.
#
#     :keyword str name: city name.
#     :keyword int province_id: province id.
#
#     :returns: list[dict(int id,
#                         str name,
#                         int province_id: province id)]
#
#     :rtype: list
#     """
#
#     return city_services.find(name, **filters)
#
#
# @api('/cities', methods=HTTPMethodEnum.POST, authenticated=False)
# def create(**options):
#     """
#     creates a city.
#
#     :param str name: city name.
#     :param int province_id: province id.
#     """
#
#     return city_services.create(**options)
#
#
# @api('/template', methods=HTTPMethodEnum.GET, authenticated=False)
# def get_template(**options):
#     return """<form method="POST">
#                   Language: <input type="text" name="language"><br>
#                   Framework1: <input type="text" name="framework"><br>
#                   Framework2: <input type="text" name="framework"><br>
#                   <input type="submit" value="Submit"><br>
#               </form>"""
#
#
# @api('/template', methods=HTTPMethodEnum.POST, authenticated=False)
# def post_template(**options):
#     return options
#
#
# @api('/test', methods=(HTTPMethodEnum.POST, HTTPMethodEnum.GET), authenticated=False)
# def test(**options):
#     d = get_current_request()
#     return dict(hash=hash(d),
#                 hash_id=hash(d.request_id))
#
#
# @api('/check', methods=HTTPMethodEnum.GET, authenticated=False, request_limit=3, lifetime=20)
# def disappearing(**options):
#     return 'I will go away soon.'
#
#
# @api('/check', methods=HTTPMethodEnum.POST, authenticated=False)
# def disappearing2(**options):
#     return 'I will stay longer.'
#
#
# @api('/old-get', methods=HTTPMethodEnum.GET, authenticated=False, request_limit=1, lifetime=1)
# def old_get(**options):
#     return 'I will go away soon.'
#
#
# @api('/old-get', methods=HTTPMethodEnum.POST, authenticated=False, request_limit=1, lifetime=1)
# def old_post(**options):
#     return 'I will go away soon.'
#
#
# @api('/old-get', methods=(HTTPMethodEnum.GET, HTTPMethodEnum.POST), authenticated=False, replace=True)
# def new(**options):
#     return url_for('demo.common.city.api.old_gets')
#
#
# @api('/url-for', methods=(HTTPMethodEnum.GET, HTTPMethodEnum.POST), authenticated=False, replace=True)
# def url(**options):
#     return url_for('demo.common.city.no_way.api.disappearing', _external=True, city_id=100)
#
#
# @api('/public', methods=HTTPMethodEnum.GET, authenticated=False)
# def public(**options):
#     return 'I am public and here to stay.'
#
#
# @api('/public-temp', methods=HTTPMethodEnum.GET, authenticated=False, request_limit=5, lifetime=40)
# def public_temp(**options):
#     return 'I am public temp and here to go 40s.'
#
#
# @api('/protected', methods=HTTPMethodEnum.GET, authenticated=True)
# def protected(**options):
#     return 'I am protected and here to stay.'
#
#
# @api('/protected-temp', methods=HTTPMethodEnum.GET, authenticated=True, request_limit=3, lifetime=120)
# def protected_temp(**options):
#     return 'I am protected temp and here to go 120s.'
#
#
# @api('/fresh', methods=HTTPMethodEnum.GET, authenticated=True)
# def fresh(**options):
#     return 'I am fresh and here to stay.'
#
#
# @api('/fresh-temp', methods=HTTPMethodEnum.GET, authenticated=True, request_limit=3, lifetime=90)
# def fresh_temp(**options):
#     return 'I am fresh temp and here to go 90s.'
#
#
# @api('/cached', methods=HTTPMethodEnum.GET, authenticated=False)
# @cached(expire=1000000)
# def cached_method(name, age, **options):
#     return DTO(name=name, age=age, **options)
#
#
# @api('/memcached', methods=HTTPMethodEnum.GET, authenticated=False)
# @memcached(expire=0)
# def memcached_method(name, age, **options):
#     return DTO(date=time.time())
#
#
# @api('/time', methods=HTTPMethodEnum.GET, authenticated=False)
# def sentry_method(**options):
#     date = options.get('date')
#     now = datetime_services.now('europe/berlin')
#     options.update(type=str(type(date)), now=now)
#     return options
