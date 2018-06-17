from datetime import date

from flask import Flask, Request, Response, jsonify, request
# from flask_sqlalchemy import Column, Date, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
@app.route('/todos/', methods = ['POST'])
def create_todo():
    todo_obj=Todo(text=request.form.get('text'),done=False)
    db.session.add(todo_obj)
    db.session.commit()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/todos/', methods=['GET'])
def get_todo():
    todos = Todo.query.all()
    todos_list = list()
    for todo in todos:
        todos_list.append(todo_schema.dump(todo).data)
    return jsonify(todos_list)
    


@app.route('/todos/<int:id_obj>/', methods=['PUT'])
def modify_todo(id_obj):
    todo_obj=Todo.query.filter_by(id = id_obj).first()
    todo_obj.done = bool(request.form.get('done'))
    # print(todo_obj.done)
    db.session.commit()
    Response = jsonify({'success':'true'})
    Response.headers.add('Access-Control-Allow-Origin', '*')
    return Response

# @app.route('/todos/<int:id>/', methods=['OPTIONS'])
# def option(id):
#     return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/todos/<int:id>/', methods=['DELETE'])
def delete_todo(id):
    Response = jsonify({'success':'true'})
    Response.headers.add('Access-Control-Allow-Origin', '*')
    todo_obj = Todo.query.get(id)
    db.session.delete(todo_obj)
    db.session.commit()
    return Response





if __name__ == '__main__':
    app.run(debug=True)