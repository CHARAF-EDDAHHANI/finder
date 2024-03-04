#!/usr/bin/env python3

#from flask import request
#from flask_restful import Resource
#from sqlalchemy.exc import SQLAlchemyError
#from app.console import Console


#class CreateEmployeeResource(Resource):
   # def post(self):
     #   try:
       #     data = request.json
       #     console = Console(g.session, None)
          #  console.create_employee(**data)
           # return {"message": "Employee created successfully"}, 201
        #except SQLAlchemyError as e:
           # g.session.rollback()
           # return {"error": "Database error", "details": str(e)}, 500
       # except Exception as e:
            #return {"error": "Internal server error", "details": str(e)}, 500
