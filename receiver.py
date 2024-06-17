import datetime
from main import db


class Request(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  data = db.Column(db.String(128), nullable=False)

  # username = db.Column(db.String(80), unique=True, nullable=False)
  # email = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
    return f'{self.data}>'


class Receiver:

  def __init__(self, endpoint_name):
    self.name = endpoint_name
    self.msgs = []

  def receive(self, data):
    self.msgs.append(data)
    with open('./text_data_db.txt', 'a+') as db:
      db.write('\n@' + str(datetime.datetime.now()) + '\n')
      db.write(data)
