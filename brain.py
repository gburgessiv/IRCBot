#!/usr/bin/env python3

import irc_callbacks
import re

"""
This is brain.py. It recieves messages and calls appropriate functions (if one exists)
in order to respond to these messages. Below is a callbacks Dict, where all of the callbacks
are linked to their triggers. 
"""
callbacks = { "hello": irc_callbacks.sayHi
            , ".random": irc_callbacks.randomNumber
            , ".help": irc_callbacks.help
            , ".man": irc_callbacks.man
            , ".py2doc": irc_callbacks.py2doc
            , ".pydoc": irc_callbacks.py3doc
            , ".py3doc": irc_callbacks.py3doc
            }

def think(sender, message):
    global callbacks

    if sender is None:
        raise ValueError("Sender is None")
    if message is None:
        raise ValueError("Message is None")

    message = message.strip()

    if re.search('\s+', message):
        cmd, args = re.split('\s+', message, 1)
    else:
        cmd = message
        args = ""

    cmd = cmd.lower()

    if cmd not in callbacks:
        return None
    else:
        try:
            result = callbacks[cmd](sender, args)
        except Exception as e:
            result = str(e)
        else:
            if result is None:
                result = ""

    return result

if __name__ == '__main__':
    # Could've used unittest, but that was a bit much for a single function
    print("Running unit tests...")
    
    ### START OF UNIT TESTS ###

    def sayHi(user, arg):
        return "Hi, " + user

    def greet(user, arg):
        return "Hello, " + arg

    def throwParty(user, arg):
        raise ValueError("Testing.")
    
    old_callbacks = callbacks

    callbacks = { "hi": sayHi,
                  "hello": sayHi,
                  "greet": greet,
                  "party": throwParty}

    assert think("", "hello world") == sayHi("", "world")
    assert think("", "hello") == sayHi("", "")
    assert think("hi", "HELLO") == sayHi("hi", "")
    assert think("hi", "HeLlO world") == sayHi("hi", "world")

    assert think("hi", "hi") == sayHi("hi", "")
    assert think("hi", "hi world") == sayHi("hi", "world")

    assert think("greet", "hi") == sayHi("greet", "")
    assert think("hi", "greet me") == greet("hi", "me")
    assert think("hi", "greet") == greet("", "")

    assert think("", "") == None

    try:
        res = think("", "party") 
        throwParty("", "")
    except ValueError as e:
        assert res == str(e)
    
    st = 'a'

    while st in callbacks:
        st += 'a'

    assert think("", st) == None

    try:
        think(None, "")
    except ValueError:
        pass
    else:
        assert False

    try:
        think("", None)
    except ValueError:
        pass
    else:
        assert False
    ### END OF UNIT TESTS ###

    print("Passed.")
    print("Say stuff and this will think about it. Your username will be \"Tester\"")

    callbacks = old_callbacks

    while True:
        z = input()
        n = think("Tester", z)
        if n:
            print(n)
