from flask import Flask
from flask_digest import Stomach

app = Flask(__name__)
stomach = Stomach('realm')

db = dict()

@stomach.register
def add_user(username, password):
    print(username, password)
    db[username] = password

@stomach.access
def get_user(username):
    return db.get(username, None)

@app.route('/')
@stomach.protect
def main():
    return '<h1> resource <h1>'

add_user('admin', '12345')
app.run()
