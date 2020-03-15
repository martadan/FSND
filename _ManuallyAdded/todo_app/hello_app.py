from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '{dialect}://{user}:{pass}@{host}:{port}/{db}'.format(**{
    'dialect': 'postgresql',
    'user': 'postgres',
    'pass': 'yT82Sb&n2mcuy',
    'host': 'localhost',
    'port': '5432',
    'db': 'mydb'
})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return '<Person {id}: {name}>'.format(**{'id': self.id, 'name': self.name})


db.create_all()


@app.route('/')
def index():
    person = Person.query.first()
    return 'Hello again, {0}!'.format(person.name)


if __name__ == '__main__':
    app.run()
