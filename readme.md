# Marvin, the IRC bot#

Marvin is a simple IRC bot, written in python. He demonstrates some aspects of
the Unix design philosophy:
* He is split into several modular components:
  * A storage part 
  * A connection part 
  * A brain, to which other parts ("callbacks") can be attached
* His code is fairly clear, divided into functions that "do one thing and do it
    well."
* His parts are separate, and don't care about each others' implementation
    details.
* He is small
* He is transparent and fairly easy to debug
* He is mostly silent. The server only outputs chat messages it receives.
* Exceptions that get raised by modules are presented in text form to the user.
    This makes marvin easy to repair when he isn't working as expected.
* He is easily extensible with callback methods.

The only major Unix design tenet that we've failed to build into Marvin is
composition: It would be difficult to chain an IRC robot to another program,
because of the nature of distributed chat programs.

Marvin also demonstrates the use of common Unix interfaces: Sockets and
files.

To activate him, run `python irc_connection.py`


## Connection ##

To deal with the actual communication with IRC, we've written a class called
`IrcConnection`. This deals with all the communication details, like joining
and leaving IRC channels, connecting to servers, and sending and receiving
messages. This is useful primarily in two ways: 

1. One could potentially take this class and use it for some other project that
  also uses IRC
2. One could build a different class that would allow Marvin to work with some
  other kind of protocol, like Jabber or Facebook Chat, and drop that class
  into the place of ours.


## Callbacks ##

An IRC bot is made up of actions that it can perform. In this case, those
actions are python functions called "callbacks." These functions are listed
in the `brain.py` file (where they're associated with commands), and enumerated
in the `irc_callbacks.py` file. We have created some demonstrative callbacks:

* help returns helpful text for other callbacks
* sayHi says hi
* randomNumber generates a random number
* man returns a link to a Unix man page on the web
* py2doc and py3doc return links to python documentation.

## Brain ##

The brain simply matches messages against a set of rules, and delegates
actions to the callbacks. It then returns their output to the IRC channel 
that sent it the message.

## Storage ##

When Marvin needs to remember something, he uses the `irc_database.py` module,
which stores data in a simple file, containing json text.
