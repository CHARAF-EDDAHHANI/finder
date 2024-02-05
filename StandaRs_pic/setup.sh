#!/bin/bash

# Create a Python 3 virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install required packages (sqlalcehemy-)
/mnt/d/finder/venv/bin/python -m pip install sqlalchemy

# Display information about the installed packages of sqlalchemy indicating successful setup
/mnt/d/finder/venv/bin/python -m pip show sqlalchemy

#display message success setup
echo "Virtual environment created and activated. You can now work within the virtual environment."

