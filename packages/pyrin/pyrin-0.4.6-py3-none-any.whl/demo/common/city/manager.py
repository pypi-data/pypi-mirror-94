# -*- coding: utf-8 -*-
"""
city manager module.
"""

from pyrin.core.structs import Manager
from pyrin.database.services import get_current_store
from pyrin.core.globals import _

import pyrin.database.paging.services as paging_services

from demo.common.city.exceptions import CityNotFoundError
from demo.common.city.models import CityEntity
from pyrin.database.transaction.contexts import atomic_context, nested_context, \
    subtransaction_context
from pyrin.database.transaction.decorators import atomic, nested, subtransaction


class CityManager(Manager):
    """
    city manager class.
    """

    def get(self, city_id, **options):
        """
        gets the specified city.

        :param int city_id: city id to get its info.

        :raises CityNotFoundError: city not found error.

        :returns: dict(int id,
                       str name,
                       int province_id: province id)

        :rtype: dict
        """

        store = get_current_store()
        city = store.query(CityEntity).get(city_id)

        if city is None:
            raise CityNotFoundError(_('City [{city_id}] not found.'
                                      .format(city_id=city_id)))

        return city.to_dict()

    def clear(self):
        store = get_current_store()
        return store.query(CityEntity).delete()

    def find(self, name, **filters):
        """
        finds cities with given filters.

        :keyword str name: city name.
        :keyword int province_id: province id.

        :returns: list[dict(int id,
                            str name,
                            int province_id: province id)]

        :rtype: list
        """

        clauses = self._make_find_clause(**filters)
        store = get_current_store()
        entities = store.query(CityEntity)\
            .filter(*clauses)\
            .order_by(CityEntity.id)\
            .paginate(**filters).all()

        return entities

    def _make_find_clause(self, **filters):
        """
        makes the required find clauses based on
        given filters and returns the clauses list.

        :keyword str name: city name.
        :keyword int province_id: province id.

        :rtype: list
        """

        clauses = []

        name = filters.get('name', None)
        province_id = filters.get('province_id', None)

        if name is not None:
            clauses.append(CityEntity.name.icontains(name))

        if province_id is not None:
            clauses.append(CityEntity.province_id == province_id)

        return clauses

    def create(self, **options):
        """
        creates a city.

        :param str name: city name.
        :param int province_id: province id.
        """

        try:
            with atomic_context() as store1:
                # store1 = get_current_store()
                city = CityEntity(name='1')
                store1.add(city)

            with atomic_context():
                city2 = CityEntity(name='FUCK')
                store2 = get_current_store()
                store2.add(city2)
                # raise Exception('FUCK')
        except:
            pass

        city3 = CityEntity(name='PARENT')
        store = get_current_store()
        store.add(city3)
        raise Exception('Im Done.')

    # def create(self, name, province_id, **options):
    #     """
    #     creates a city.
    #
    #     :param str name: city name.
    #     :param int province_id: province id.
    #     """
    #
    #     self.a()
    #     self.b()
    #
    #     city3 = CityEntity(name='fake')
    #     store = get_current_store()
    #     store.add(city3)
    #     raise Exception('Im Done.')
    #
    # @atomic
    # def a(self):
    #     store1 = get_current_store()
    #     city = CityEntity(name='1')
    #     store1.add(city)
    #
    # @atomic
    # def b(self):
    #     city2 = CityEntity(name='2')
    #     store2 = get_current_store()
    #     store2.add(city2)

    # def create(self, name, province_id, **options):
    #     """
    #     creates a city.
    #
    #     :param str name: city name.
    #     :param int province_id: province id.
    #     """
    #
    #     store1 = get_current_store()
    #     city = CityEntity(name='1')
    #     store1.add(city)
    #     a = 0
    #     #store1.commit()
    #
    #     store2 = get_current_store()
    #     city2 = CityEntity(name='2')
    #     store2.add(city2)
    #     # #store2.commit()
    #     #
    #     city3 = CityEntity(name='fake')
    #     store3 = get_current_store()
    #     store3.add(city3)
    #     # # raise Exception('Im Done.')
