import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.engine.url import URL

db_params = {
    'drivername': 'postgresql',
    'username': 'postgres',
    'password': 'yT82Sb&n2mcuy',
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'todoapp'
}

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = URL(**db_params)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yT82Sb&n2mcuy@127.0.0.1:5432/todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_lists.id'), nullable=False)

    def __repr__(self):
        return f'<TODO item {self.id}: {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todo_lists'
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='todo_list', lazy=True)

    def __repr__(self):
        return f'<TODO list {self.id}: {self.list_name}'


# db.create_all()


@app.route('/')
def index():
    # return render_template(
    #     'index.html',
    #     data=Todo.query.order_by('id').all()
    # )
    return redirect(url_for('get_list_todos', list_id=1))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template(
        'index.html',
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    )


@app.route('/todos/<todo_id>/delete-item', methods=['POST'])
def delete_item(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        # description = request.form.get('description', '')
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)
        # return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
