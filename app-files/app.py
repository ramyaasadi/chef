from flask import Flask, request
from flask import Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import dicttoxml

#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

e = create_engine('sqlite:///salaries.db')

app = Flask(__name__)
api = Api(app)

class Departments_Meta(Resource):
    def get(self):
        #Connect to databse
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct DEPARTMENT from salaries")
        return {'departments': [i[0] for i in query.cursor.fetchall()]}

class Departmental_Salary(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from salaries where Department='%s' limit 20"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        #result = query.fetchall()
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        xml = dicttoxml.dicttoxml(result)

        #result = '<?xml version="1.0" encoding="UTF-8"?><note><to>Tove</to><from>Jani</from><body>Don\'t forget me this weekend!</body></note>'
        # result.headers["Content-Type"] = "application/xml"
        #return Response(result, mimetype='text/xml')
        return Response(xml, mimetype='text/xml')
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
 
api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments')

if __name__ == '__main__':
     app.run()
