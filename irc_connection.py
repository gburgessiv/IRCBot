import socket

class IrcConnection(object):
  def __init__(self, host, port=6667, channels=[], nick="marvin", password=None, fullname="Marvin", servname="unknown"):
    self.host = host
    self.port = port
    self.nick = nick
    self.password = password
    self.fullname = fullname
    self.servname = servname

    self.connect()

    found = False
    while not found:
      data = self.connection.recv(4096).decode('ascii').splitlines()
      print(data)
      for datum in data:
        if datum.split()[0] == "PING":
          self.sendMessage("PONG " + ' '.join(datum.split()[1:]))
          found = True

    for channel in channels:
      self.joinChannel(channel);

  def readFromConnection(self):
    if not self.connection:
      raise IOError("Cannot read messages unless connected to server")
    data = self.connection.recv(4096)
    if data:
      return data.decode('ascii').splitlines()
    else:
      return None

  def connect(self):
    self.connection = socket.create_connection((self.host, self.port))
    self.sendMessage("NICK " + self.nick)
    self.sendMessage("USER " + self.nick + " " + self.host + " " + self.servname + " :" + self.fullname)
    if self.password:
      self.sendMessage("PASS " + self.password)

  def sendMessage(self, message):
    print(message)
    self.connection.send((message + "\r\n").encode('ascii'))

  def joinChannel(self, channel):
    self.sendMessage("JOIN " + channel)

  def getNextMessages(self):
    received = None
    while not received:
      for message in self.readFromConnection():
        components = message.split()
        if components[0] == "PING":
          self.sendMessage("PONG " + ' '.join(components[1:]))
        elif components[1] == "PRIVMSG":
          received = (components[0].split("!")[0].lstrip(':'), 
                      components[2], 
                      ' '.join(components[3:]).lstrip(':'))

    return received;




con = IrcConnection("earth.benwr.net", channels=["#test"])

while True:
  response = con.getNextMessages()
  print(response)
