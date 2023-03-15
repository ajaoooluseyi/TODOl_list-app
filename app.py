from flask import Flask, request, jsonify, make_response #imports Flask web module
from flask_sqlalchemy import SQLAlchemy  #imports SQLAlchemy module to connect to database
from flask_restful import Resource, Api
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema #imports modules to serialize Python objects


app = Flask(__name__)
api = Api(app)
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
class TodoSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model =  Todo
        load_instance = True

#GET endpoint
class GetToDo(Resource):
    def get(self):
        get_list = Todo.query.all()  # queries all the todos from database
        encoder = TodoSchema(many = True)
        todos = encoder.dump(get_list)   # serializes objects from SQLAlchemy

        return make_response(jsonify({'todos':todos})) #returns list of todos as JSON

class GetToDoById(Resource):
    def get(self, id):
        get_todo = Todo.query.get(id) # queries all the todos from database by given id
        encoder = TodoSchema()
        todo = encoder.dump(get_todo)

        return make_response(jsonify({"todo": todo}))

class AddTask(Resource):
    def post(self):
        if request.is_json:
            data = request.get_json()  # gets data from request body
            complete = data["complete"]
            text = data["text"]

            new_task = Todo(text=text, complete = complete)
            db.session.add(new_task) # adds task to database
            db.session.commit() # commits changes to database

            encoder = TodoSchema()
            task = encoder.dump(new_task)


            return make_response(jsonify({'todo':task}), 200)
        else:
            return {'error': 'Request not JSON'}, 400

class UpdateTask(Resource):
    def put(self, id):
        if request.is_json:
            data = request.get_json() # gets data from request body
            get_todo = Todo.query.get(id) # queries all the todos from database by given id

            if get_todo is None:
                return  {'error': "Not found"}, 400
            else:
                get_todo.text = data["text"] #updates text with new text

                db.session.commit() # commits changes to database
                return 'Updated', 200
        else:
            return {"error": "Request is not JSON"}, 400

class ChangeTaskStatus(Resource):
    def patch(self, id):
        if request.is_json:
            get_todo = Todo.query.get(id) # queries all the todos from database by given id
            data = request.get_json()

            if get_todo is None:
                return  {'error': "Not found"}, 400
            else:
                get_todo.complete = data["complete"] #updates text with new text
                db.session.commit() # commits changes to database

                return 'Updated', 200
        else:
            return {'error':"Request is not JSON"}

class DeleteTask(Resource):
    def delete(self, id):
        todo = Todo.query.get(id)  # queries all the todos from database by given id
        if todo is None:
            return  {'error': "Not found"}, 400
        else:
            db.session.delete(todo) # deletes task from database
            db.session.commit()  # commits changes to database
            return 'Task deleted', 200

api.add_resource(GetToDo, "/")
api.add_resource(GetToDoById, "/<int:id>")
api.add_resource(AddTask, "/")
api.add_resource(UpdateTask, "/<int:id>")
api.add_resource(ChangeTaskStatus, "/<int:id>")
api.add_resource(DeleteTask, "/<int:id>")





if __name__ == "__main__":
    app.run(debug=True, port=8001)
