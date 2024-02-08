#!/usr/bin/env python3

from sqlalchemy import create_engine, inspect

DATABASE_URL = 'sqlite:///appengine/finder.db'  # Update the path to your finder.db
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# Get the table names
table_names = inspector.get_table_names()

print("Table Names:")
for table_name in table_names:
    print(table_name)

