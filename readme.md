# Marvin, the IRC bot #
Marvin is a simple IRC bot, written in python.

To activate him, you'll probably want to configure him first. Otherwise, he won't
be very useful.

 If you're new to IRC, you should read 
[this introduction](http://www.irchelp.org/irchelp/new2irc.html) before trying
it out. I'd recommend installing XChat (or [Colloquy](http://colloquy.info) if
you're on OS X). XChat can almost certainly be installed via your package
manager ([or from here, if you're on Windows](http://www.silverex.org/download/)).

If you're evaluating Marvin for the Virginia Tech Intro to Unix class, you'll
probably want to join us in the #ece2524 channel of the OFTC IRC network. We have
an instance of marvin running there. If you're planning to run your own version
of marvin, please don't join this channel, as all the marvins will try to talk
at once.

To join us, simply tell your IRC client to connect to irc.oftc.net, and to join
the #ece2524 channel.

## Design Philosophy ##
Marvin demonstrates some aspects of the Unix design philosophy:
* He is split into several modular components:
  * A storage part (irc_database.py) 
  * An IRC connection class (irc_connection.py)
  * A brain, to which other parts ("callbacks") can be attached (brain.py)
  * "Callbacks", which store modules of various functions that can be called by
    the brain 
* His code is fairly clear, divided into functions that "do one thing and do it
    well." 
* His parts are separate, and don't care about each others' implementation
    details.
* He is small, because library methods are used for most non-IRC tasks and there
    is no GUI
* Ease of use is favored over efficiency, as the bottleneck is not hardware but
    rate-limiting on IRC networks.
* He is transparent and fairly easy to debug, due to an optional debug flag in
    the IRCConnection constructor. The database is stored in plain text files
    to reduce overhead.
* He is mostly silent. The bot does not send unnecessary information over IRC.
* Exceptions that get raised by modules are presented in text form to the user.
    This makes marvin easy to repair when he isn't working as expected.
* He is written in python3, and is therefore portable across many OSes.
* He is easily extensible with callback methods.

The only major Unix design tenet that we've failed to build into Marvin is
composition: It would be difficult to chain an IRC robot to another program,
because of the nature of distributed chat programs.

Marvin also demonstrates the use of common Unix interfaces: sockets and
textual files.

## Dependencies ##
* python (2.x or 3.x)

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

* .help returns helpful text for other callbacks
* .sayHi says hi
* .random generates a random number
* .man returns a link to a Unix man page on the web
* .py2doc and py3doc return links to python documentation.

Callbacks start with a dot to avoid collisions with other bots. (It's common
practice for IRC bots to contain a unique character not used by other bots in
the channel at the start of their trigger strings.)

## Brain ##

The brain simply matches messages against a set of rules, and delegates
actions to the callbacks. It then returns their output to the IRC channel 
that sent it the message.

## Storage ##

When Marvin needs to remember something, he uses the `irc_database.py` module,
which stores data in a simple file, containing json text.

## Additional Documentation ##
* RFC1459 - http://irchelp.org/irchelp/rfc/rfc.html
* RFC2812 - http://tools.ietf.org/html/rfc2812#section-3.2.2
