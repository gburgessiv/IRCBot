import socket
import brain

class IrcConnection(object):
  debug = 1

  #TODO move to config file

  def __init__(self, host, port=6667, channels=[''], nick="marvin", password=None, fullname="Marvin", servname="unknown"):
    self.host = host
    self.port = port
    self.nick = nick
    self.password = password
    self.fullname = fullname
    self.servname = servname

    self.connect()

    self.channels = []
    for channel in channels:
      self.channels.append(channel)
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

    if self.password:
      self.sendMessage("PASS " + self.password)

    self.sendMessage("NICK " + self.nick)

    self.sendMessage("USER " + self.nick + " " + self.host + " " + self.servname + " :" + self.fullname)

    # UnrealIRCD doesn't let you do anything until you respond to a PING.
    # Waiting for a PING may be a reasonable thing to do anyway.
    data = self.readFromConnection()
    for datum in data:
      if datum.split()[0] == "PING":                            # PING sometext
        self.sendMessage("PONG " + ' '.join(datum.split()[1:])) # PONG sometext


  # Quits IRC and disconnects the socket.
  def disconnect(self, message=''): 
    self.sendMessage("QUIT :" + message)
    self.connection.shutdown(socket.SHUT_RDWR)
    self.connection.close()

  def sendMessage(self, message):
    self.connection.send((message + "\r\n").encode('ascii'))
    

  def joinChannel(self, channel):
    self.sendMessage("JOIN " + channel)
    self.channels.append(channel)

  def partChannel(self, channel, message=''):
    if channel in self.channels:
      self.sendMessage("PART " + channel + " :" + message)
    else:
      raise NameError("Can't part from channel I'm not in.")

  def getNextChat(self):
    received = None
    while not received:               # Haven't met a PRIVMSG yet
      for message in self.readFromConnection():
        components = message.split()
        if components[0] == "PING":   # Need to respond to PINGS
          pongString = "PONG" + ' '.join(components[1:])
          self.sendMessage(pongString)
          if debug:
            print(pongString)
        elif len(components) > 1 and components[1] == "PRIVMSG":
          received = (components[0].split("!")[0].lstrip(':'),  # nick
                      components[2],                            # target
                      message)                                 # message

    return received;

  def sendChat(self, target, message):
    self.sendMessage("PRIVMSG " + target + " :" + message)

  def quit(self):
    self.sendMessage("QUIT")
    self.connection.shutdown(socket.SHUT_RDWR)
    self.connection.close()



if __name__ == "__main__":
  #TODO move data to config file
  con = IrcConnection("irc.oftc.net", channels=["#dyreshark"])
  
  while True:
    response = con.getNextChat()
    print(response)
    # Sender, message
    res = brain.think(response[0], response[2])
    
    if res:
      con.sendChat(response[1], res)
