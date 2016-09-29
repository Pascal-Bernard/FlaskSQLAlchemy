

#-------------------------------参考=http://www.pythondoc.com/Flask-RESTful/quickstart.html---------------------------------#
from flask import Flask, request
from flask.ext.restful import Resource, Api
from flask.ext.restful import reqparse

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
   
    
'''
# get request parametres =>
parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate to charge for this resource')
args = parser.parse_args()
'''







