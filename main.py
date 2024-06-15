import os
import time

from flask import Flask
from receiver import Receiver

title = os.environ['Title'] = 'DEV_MODE'
# os.environ.get('Title')

app = Flask(__name__)
# os.environ
# TODO
# are there any feature requests?
# would like an app to: display current time [mat]


@app.route('/')
def index():
    return f'Welcome to this website.<br/>\
    # Current title: {title}<br/>\
    page loaded at: {time.time()} '

    # Question (Task): what does time() function return?


@app.route('/receiver')
def receiver_endpoint():
    receiver = Receiver('ear')
    receiver.receive(input())
    return 'Not yet implemented'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
