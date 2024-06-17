import datetime
import os
import time

from flask import Flask, render_template, request
from flask.helpers import redirect
from flask_sqlalchemy import SQLAlchemy

# from receiver import Receiver, Request
from db import Request, SessionLocal

title = os.environ['Title'] = 'DEV_MODE'
# os.environ.get('Title')

app = Flask(__name__)
# db = get_db()
# db = SQLAlchemy(app)
# os.environ
# TODO
# are there any feature requests?
# would like an app to: display current time [mat]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.route('/plan')
def doc():
    return render_template('doc.html')


@app.route('/receiver/receive', methods=['POST'])
def handle_data():
    data = request.form['text_data']
    if data:
        #TODO
        with SessionLocal() as db:
            new_req = Request(data=data)
            db.add(new_req)
            db.commit()
        # receiver = Receiver('text_data')
        # receiver.receive(data)

    return redirect('/list')
    return f'Hello, {data}! Your data was submitted successfully.\
    <a href="/receiver">Receiver</a>'


@app.route('/')
def index():
    #DEV: temporarily: redirect root path (/) to /receiver
    return redirect('/receiver')
    return f'Welcome to this website.<br/>\
    # Current title: {title}<br/>\
    page loaded at: {time.time()} '

    # Question (Task): what does time() function return?


@app.route('/receiver', methods=['GET'])
def receiver_endpoint():

    return render_template('receiver.html')


@app.route('/list', methods=['GET'])
def messages():
    # with open('./text_data_db.txt', 'r') as db:
    #     db.readline()
    #     data = db.readlines()
    #     result = [(data[i], data[i + 1]) for i in range(0, len(data) - 1, 2)]
    result = []
    with SessionLocal() as db:
        result = db.query(Request).all()
        print(result)
    return render_template('list.html', data=reversed(result))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
