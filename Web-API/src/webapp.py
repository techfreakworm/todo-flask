from datetime import date

from flask import Flask, Request, Response, jsonify
# from flask_sqlalchemy import Column, Date, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
CORS(app)

db = SQLAlchemy(app)

#marsh = Marshmallow(app)

######### MODEL: Todo #########
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column('text', db.String(250))
    done = db.Column('done', db.Boolean)

    def __repr__(self):
        return '<Todo %r>' % self.text

class TodoSchema(ModelSchema):
    class Meta:
        model = Todo
        # sql_session = db.session



todo_schema = TodoSchema()


##### CREATE SCHEMA ######
db.create_all()


########### ROUTING AND API CALLS ###########
@app.route('/todos/', methods = ['PUT'])
def create_todo():
    # data = Request.data
    # todo_obj = Todo()
    # todo_obj.text = data.text
    # todo_obj.done = data.done
    # db.session.add(todo_obj)
    # db.session.commit()
    return True

@app.route('/todos/', methods=['GET'])
def get_todo():
    todos = Todo.query.all()
    todos_list = list()
    for todo in todos:
        todos_list.append(todo_schema.dump(todo).data)
    return jsonify(todos_list)
    

@app.route('/todos/<id>', methods=['PUT'])
def modify_todo():
    return "something"

@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo():
    return "something"





if __name__ == '__main__':
    app.run(debug=True)