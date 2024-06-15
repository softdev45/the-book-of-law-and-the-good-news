import datetime


class Receiver:

  def __init__(self, endpoint_name):
    self.name = endpoint_name
    self.msgs = []

  def receive(self, data):
    self.msgs.append(data)
    with open('text_data_db.txt', 'a+') as db:
      db.write('\n@' + str(datetime.datetime.now()) + '\n')
      db.write(data)
