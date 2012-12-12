import random
import re

def help(sender, topic):
    # If this gets sooper-big, we can just have it automatically
    # put together help based on docstrings
    helptopics = { "random": ".random [max|min-max]: " +
                             "Generates a random number from 0 to 1000." + 
                             " Minimum and maximum are specifiable." + 
                             " No negatives plz"
                 , "man": ".man man_page: " +
                          "Gets a link to the requested manpage."
                 , "py2doc": ".py2doc module: " +
                             "Gets python2 documentation for the requested module"
                 , "py3doc": ".py3doc module: " +
                             "Gets python3 documentation for the requested module"
                 , "pydoc": "Alias for py3doc" } 

    # If they started the topic with a ., ignore it.
    if topic.startswith('.'):
        topic = topic[1:]

    topic = topic.lower()

    if not topic:
        res = "I'm a bot! And I can do the following (type .help <topic> for info): "
        res += ', '.join(helptopics.keys())
    elif topic in helptopics:
        res = helptopics[topic]
    else:
        res = "Invalid topic."

    return "{}, {}".format(sender, res)

def sayHi(sender, _):
    return "Hello, {}!".format(sender)

def _tryParse(string, default, targtype = int):
    try:
        return targtype(string)
    except:
        return default

def randomNumber(sender, rest):
    rest = rest.strip()

    lowlimit = 0
    uplimit = 1000

    # if rest isn't empty
    if rest:
        # ignore everything but the first "word"
        rest = re.split('\s+', rest, maxsplit = 1)[0]
        
        # if both lower and upper limit were specified
        if rest.find('-') != -1:
            low, rest = rest.split('-', 1)
            lowlimit = _tryParse(low, lowlimit)

        uplimit = _tryParse(rest, uplimit)

        if lowlimit == uplimit:
            return "{}, that's not very random.".format(sender)

        # we allow "backward" ranges
        if lowlimit > uplimit:
            t = uplimit
            uplimit = lowlimit
            lowlimit = t

    return "{}: {}".format(sender, random.randint(lowlimit, uplimit))

def man(sender, msg):
  args = msg.split()
  fmt = "{}: http://www.freebsd.org/cgi/man.cgi?sektion={}&query={}&apropos={}"
  if len(args) > 1:
    if args[0] == "-k":
      return fmt.format(sender, 0, args[1], 1)
    else:
      return fmt.format(sender, args[0], args[1], 0)
  else:
    return fmt.format(sender, 0, args[0], 0)

def py2doc(sender, module):
    return "{}: http://docs.python.org/2/library/{}.html".format(sender, module)

def py3doc(sender, module):
    return "{}: http://docs.python.org/3/library/{}.html".format(sender, module)
