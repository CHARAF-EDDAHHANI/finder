#!/usr/bin/env python3

#import necessary modules
import sys
import json
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#define a base class for declarative models
Base = declarative_base()

#define a base model with common attributes and methods
class BaseModel(Base):
    #this class is abstract and will not be used to create database tables directly
    __abstract__ = True

    # common fields for all models : created_at updated_at timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    #method to convert model instance to dictionary
    def to_dict(self):
        #returns a dict containing column name-value pairs for each column
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    #method to create a model instance from a dict
    @classmethod
    def from_dict(cls, data):
         # Creates a new instance of the class using the provided dictionary data
        return cls(**data)
        
    # Constructor method for the base model 
    def __init__(self, *args, **kwargs):
    # Calls the constructor of the superclass (declarative_base) with any provided arguments
        super(BaseModel, self).__init__(*args, **kwargs)

    # Method to update the 'updated_at' timestamp
    def update_timestamp(self):
        # Updates the 'updated_at' timestamp to the current datetime
        self.updated_at = datetime.now()
