#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Core chiron library function

Defines the Message object for protocol modules to subclass, a standard
collection of fetcher functions, and the core MatchEngine.
"""

from __future__ import print_function, unicode_literals

import datetime
import re
import time

from .fetchers import fetch_trac

SEEN_TIMEOUT = 5 * 60

# There's a lot of missing docstring warnings. Disable them all for the
# moment, until I get around to dealing.
#pylint:disable=missing-docstring

class Message(object):
    def log_arrival(self, ):
        print('%s: -c %s -i "%s": %s -> %s' % (
            datetime.datetime.now(),
            self.cls(), self.instance(),
            self.sender(), self.recipient(),
        ))

    def body(self):
        raise NotImplementedError

    def cls(self):
        raise NotImplementedError

    def instance(self): #pylint:disable=no-self-use
        return ""

    def sender(self):
        raise NotImplementedError

    def recipient(self):
        raise NotImplementedError

    def is_personal(self):
        raise NotImplementedError

    def skip_message(self):
        """Returns whether this message should be skipped

        At a minimum, this probably needs to recognize messages from Chiron,
        to avoid reply loops."""
        raise NotImplementedError

    def context(self, ):
        # We have default fetchers for some classes. This adds two more ways
        # to trigger default fetchers behavior:
        # - test classes (for easier testing of defaults)
        # - instanced personals (to facilitate looking up many tickets for one project)
        if "-test" in self.cls() or self.is_personal():
            return self.instance()
        return self.cls()

    def send_reply(self, messages):
        raise NotImplementedError

def build_matcher(regex, flags=0):
    regex = re.compile(regex, flags)
    def match(msg):
        return regex.finditer(msg.body())
    return match


def subspan(arg1, arg2):
    """Return whether the (x,y) range indicated by arg1 is entirely contained in arg2

    >>> subspan((1,2), (3,4))
    False
    >>> subspan((1,3), (2,4))
    False
    >>> subspan((3,4), (1,2))
    False
    >>> subspan((2,4), (1,3))
    False
    >>> subspan((1,4), (2,3))
    False
    >>> subspan((2,3), (1,4))
    True
    >>> subspan((1,4), (1,4))
    True
    """
    if arg1 == arg2: # ignores two identical matching strings
        return True
    beg1, end1 = arg1
    beg2, end2 = arg2
    return (beg1 >= beg2) and (end1 <= end2) and ((beg1 != beg2) or (end1 != end2))

class MatchEngine(object):
    def __init__(self, ):
        self.classes = []
        self.fetchers = {}
        self.matchers = []
        self.last_seen = {}
        self.ignore_personals = False

    def add_classes(self, classes):
        self.classes.extend(classes)

    def add_fetchers(self, fetchers):
        for name, fetcher in fetchers.items():
            assert name not in self.fetchers
            self.fetchers[name] = fetcher

    def add_matcher(self, fetcher, regexp, cond=False, classes=True, flags=re.I, ):
        #pylint:disable=too-many-arguments
        assert fetcher in self.fetchers
        if cond:
            pass
        elif classes is True:
            cond = lambda m: True
        else:
            cond = lambda m: bool([cls for cls in classes if cls in m.context()])
        self.matchers.append((fetcher, [build_matcher(regexp, flags)], cond))

    def add_trac(self, name, url, classes=None):
        lname = name.lower()
        if classes is None:
            classes = [lname]
        assert name not in self.fetchers
        self.fetchers[name] = fetch_trac(url)
        self.add_matcher(name, r'\b%s[-\s:]*#([0-9]{1,5})\b' % (lname, ))
        self.add_matcher(name, r'\btrac[-\s:]*#([0-9]{1,5})\b', classes=classes)
        # The "-Ubuntu" bit ignores any "uname -a" snippets that might get zephyred
        self.add_matcher(name, r'#([0-9]{2,5})\b(?!-Ubuntu)', classes=classes)

    def find_ticket_info(self, msg):
        tickets = []
        for tracker, matchers, cond in self.matchers:
            if cond(msg):
                for matcher in matchers:
                    for match in matcher(msg):
                        span = match.span()
                        # If the text matched by this matcher is a subset of
                        # that matched for by any other matcher, skip this one
                        if any(subspan(span, span1) for tracker1, fetcher1, t1, span1 in tickets):
                            print("  -> ignoring tracker %s with smaller span %s" % (tracker, span))
                            continue
                        # Remove from tickets any whose text is a subset of
                        # this one's matched text.
                        tickets = [t1 for t1 in tickets if not subspan(t1[3], span)]
                        # Add this matcher
                        tickets.append((tracker, self.fetchers[tracker], match.group(1), span))
        return tickets

    def process(self, msg, ):
        msg.log_arrival()
        if msg.skip_message():
            print("  -> skipping message from %s" % (msg.sender(), ))
            return
        if self.ignore_personals and msg.is_personal():
            print("  -> ignoring personal")
            return
        tickets = self.find_ticket_info(msg)
        messages = format_tickets(self.last_seen, msg, tickets)
        msg.send_reply(messages)

def format_tickets(last_seen, msg, tickets):
    messages = []
    for tracker, fetcher, ticket, span in tickets:
        print("  -> Found ticket: %s, %s (span: %s)" % (tracker, ticket, span))
        age_key = (tracker, ticket, msg.cls()) if not msg.is_personal() else None
        old_enough = (last_seen.get(age_key, 0) < time.time() - SEEN_TIMEOUT)
        # for personals, don't bother tracking age
        if old_enough or msg.is_personal():
            url, name = fetcher(ticket)
            if not name:
                name = 'Unable to identify ticket %s' % ticket
            message = '%s ticket %s: %s' % (tracker, ticket, name)
            messages.append((message, url))
            last_seen[age_key] = time.time()
    return messages
