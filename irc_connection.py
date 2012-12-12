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
    #found = False
    #while not found:
    #  data = self.readFromConnection()
    #  for datum in data:
    #    if datum.split()[0] == "PING":                            # PING sometext
    #      self.sendMessage("PONG " + ' '.join(datum.split()[1:])) # PONG sometext
    #      found = True


  def sendMessage(self, message):
    self.connection.send((message + "\r\n").encode('ascii'))
    

  def joinChannel(self, channel):
    self.sendMessage("JOIN " + channel)
    self.channels.append(channel)

  def partChannel(self, channel):
    if channel in self.channels:
      self.sendMessage("PART " + channel)
    else:
      raise NameError("Can't part from channel I'm not in.")

  def getNextChat(self):
    received = None
    while not received:               # Haven't met a PRIVMSG yet
      for message in self.readFromConnection():
        components = message.split()
        if components[0] == "PING":   # Need to respond to PINGS
          self.sendMessage("PONG " + ' '.join(components[1:]))

        elif components[1] == "PRIVMSG":
          message = ' '.join(components[3:])
          if message[0] == ':':
            message = message[1:]

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
  con = IrcConnection("irc.oftc.net", channels=["#dyreshark"], nick="mireshabwrose")

  while True:
    response = con.getNextChat()
    print(response)
    if response[2] == con.nick + ": hello":
      con.sendChat(response[1], "howdy, " + response[0] + "!")
    elif response[2] == ".rejoin":
      con.quit()
      con = IrcConnection("irc.oftc.net", channels=["#dyreshark"], nick="mireshabwrose")

