from sqlalchemy import Integer, Unicode

from pyrin.core.globals import SECURE_FALSE, SECURE_TRUE
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn


class PersonEntity(CoreEntity):
    _table = 'person_test'
    r_id = CoreColumn(name='id', type_=Integer, primary_key=True,
                      autoincrement=False, allow_write=False)
    _r_id = CoreColumn(name='_id', type_=Integer, primary_key=True,
                       autoincrement=False)
    rw_name = CoreColumn(name='name', type_=Unicode)
    _rw_name = CoreColumn(name='_name', type_=Unicode)
    w_age = CoreColumn(name='age', type_=Integer, allow_read=False)
    h_code = CoreColumn(name='code', type_=Integer, allow_read=False, allow_write=False)


person = PersonEntity()
person.r_id = 1
person._r_id = 2
person.rw_name = 'mark'
person._rw_name = 'junior'
person.w_age = 25
person._w_age = 30
person.h_code = 500

r_columns = person.readable_columns
w_columns = person.writable_columns
columns = person.all_columns
r_pk = person.readable_primary_key_columns
w_pk = person.writable_primary_key_columns
pk = person.primary_key_columns
z = 0

res = person.to_dict()
res_all = person.to_dict(readable=SECURE_FALSE)
fr = PersonEntity(**res_all)
fr_all = PersonEntity()
fr_all.from_dict(**res_all, writable=SECURE_FALSE)
fr_ALL = PersonEntity(**res_all, populate_all=SECURE_TRUE)
c = PersonEntity.rw_name.fullname
c2 = PersonEntity.r_id.fullname
v = 0