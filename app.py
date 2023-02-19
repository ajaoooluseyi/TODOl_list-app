from flask import Flask, request, jsonify, make_response #imports Flask web module
from flask_sqlalchemy import SQLAlchemy  #imports SQLAlchemy module to connect to database
from datetime import datetime
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field #imports modules to serialize Python objects


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#creating Todo table in database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False )
    complete = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
            return f"{self.text} | status - {self.complete}"

#definimg class to return JSON from python objects
class TodoSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model =  Todo
        sqla_session = db.session

    id = fields.Number(dump_only = True)
    text = fields.String(required = True)
    complete = fields.Boolean(required = True)
    date_created = fields.DateTime(dump_only = True)

#GET endpoint
@app.route('/todo', methods = ['GET'])
def read():
    get_list = Todo.query.all()  # queries all the todos from database
    encoder = TodoSchema(many = True)
    todos = encoder.dump(get_list)   # serializes objects from SQLAlchemy

    return make_response(jsonify({'todos':todos})) #returns list of todos as JSON

@app.route('/todo/<id>', methods=['GET'])
def read_by_id(id):
    get_todo = Todo.query.get(id) # queries all the todos from database by given id
    encoder = TodoSchema()
    todo = encoder.dump(get_todo)
    return make_response(jsonify({"todo": todo}))

#POST endpoint
@app.route('/todo', methods = ['POST'])
def create_todo():
    data = request.get_json()  # gets data from request body
    complete = data['complete']
    text = data['text']

    new_task = Todo(text=text, complete = complete)
    db.session.add(new_task) # adds task to database
    db.session.commit() # commits changes to database

    encoder = TodoSchema()
    todo = encoder.load(data)
    task = encoder.dump(todo) # creates new task todo

    print(task)
    return make_response(jsonify({'todo':task}), 200)

#PUT endpoint
@app.route('/todo/<id>/', methods = ['PUT'])
def update(id):
    data = request.get_json() # gets data from request body
    get_todo = Todo.query.get(id) # queries all the todos from database by given id

    if data['text']:
        get_todo.text = data["text"] #updates text with new text

    db.session.add(get_todo) # adds task to database
    db.session.commit() # commits changes to database
    encoder = TodoSchema(only=['id', 'text', 'complete']) # serializes objects for SQLAlchemy
    todo = encoder.dump(get_todo)
    return make_response(jsonify({'todo':todo}))

#DELETE endpoint
@app.route('/todo/<id>/', methods = ['DELETE'])
def delete(id):
    todo = Todo.query.get(id)  # queries all the todos from database by given id
    db.session.delete(todo) # deletes task from database
    db.session.commit()  # commits changes to database
    return make_response("", 204)

#PATCH endpoint
@app.route('/todo/<id>/', methods = ['PATCH'])
def mark_task(id):
    get_todo = Todo.query.get(id) # queries all the todos from database by given id
    data = request.get_json()

    get_todo.complete = data['complete']
    print(get_todo)
    db.session.add(get_todo) # adds task to database
    db.session.commit() # commits changes to database

    encoder = TodoSchema(only=['id', "text", 'complete']) # serializes objects for SQLAlchemy
    todo = encoder.dump(get_todo)

    return make_response(jsonify({'todo':todo}))


if __name__ == "__main__":
    app.run(debug=True)
