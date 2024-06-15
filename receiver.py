class Receiver:
 def __init__(self, endpoint_name):
  self.name = endpoint_name
  self.msgs = []

 def receive(self, msg):
  self.msgs.append(msg)
