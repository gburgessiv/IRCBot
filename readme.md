# Marvin, the IRC bot#

Marvin is a simple IRC bot, written in python. He demonstrates some aspects of
the Unix design philosophy:
* He is split into several modular components:
  * A storage part 
  * A connection part 
  * A brain, to which other parts ("callbacks") can be attached
* His code is fairly clear, divided into functions that "do one thing and do it well."
* His parts are separate, and don't care about each others' implementation details.
* He is small
* He is transparent and fairly easy to debug
* He is mostly silent. The server only outputs chat messages it receives.
* Exceptions that get raised by modules are presented in text form to the user.
    This makes marvin easy to repair when he isn't working as expected.
* He is easily extensible with callback methods.

The only major Unix design tenet that we've failed to build into Marvin is
composition: It would be difficult to chain an IRC robot to another program,
because of the nature of distributed chat programs.

To activate him, run "python irc_connection.py"
