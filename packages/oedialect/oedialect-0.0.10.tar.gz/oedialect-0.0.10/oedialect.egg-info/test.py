# -*- coding: utf-8 -*-
""" Retrieves different load areas via the oedialect module.

Notes
-----

Sources
-------
https://github.com/OpenEnergyPlatform/oedialect/blob/master/doc/example/oedialect_basic_example.ipynb

"""

import oedialect

import sqlalchemy as sa
#import geopandas as gp
#import matplotlib.pyplot as plt

#import os # for folder creation

from sqlalchemy.orm import sessionmaker
from egoio.db_tables.demand import EgoDpLoadarea

# https://docs.sqlalchemy.org/en/13/core/engines.html
engine = sa.create_engine(
        #'postgresql+oedialect://openenergy-platform.org')
        'postgresql+oedialect://localhost:8000')

# https://docs.sqlalchemy.org/en/13/orm/session_basics.html
session = sessionmaker(bind=engine)()

# https://docs.sqlalchemy.org/en/13/orm/query.html
# A1. Flensburg - this works
#query = session.query(EgoDpLoadarea).\
#        filter(EgoDpLoadarea.ags_0 == '01001000')  # Amtl. Gemeindeschluessel Flensburg

# A2. Flensburg - this does not work
query = session.query(EgoDpLoadarea).\
        filter(EgoDpLoadarea.nuts.like('DEF0%')) # NUTS code of Flensburg DEF01

# B. Schleswig-Holstein - this does not work
#query = session.query(EgoDpLoadarea).\
#        filter(EgoDpLoadarea.nuts.like('DEF0%'))  # NUTS code of Schleswig-Holstein DEF0

# C. all loadareas - does not work - too much data? kernel died.
#query = session.query(EgoDpLoadarea)

for result in query.yield_per(100):
        print(result.nuts)

print("Done")