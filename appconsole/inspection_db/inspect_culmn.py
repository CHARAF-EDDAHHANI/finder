#!/usr/bin/env python3

from sqlalchemy import create_engine, inspect

DATABASE_URL = 'sqlite:///appengine/finder.db'
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

# Get the columns of the 'employees' table
columns = inspector.get_columns('employees')

# Print column information
for column in columns:
    print(column['name'], column['type'])

