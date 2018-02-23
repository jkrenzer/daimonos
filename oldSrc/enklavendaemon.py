#!/usr/bin/python3

# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import sys
import collections
import logging
import getpass

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import locale
locale.setlocale(locale.LC_TIME, "de_DE")
import json
import re
import schedule

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

month_elements = ["Mercurium", "Sal", "Aer", "Aether", "Sulfur", "Ignis", "Crucibulum", "Cera", "Terra", "Adamas", "Mortarium", "Aqua"]
day_sovereigns = ["Mond", "Mars", "Merkur", "Jupiter", "Venus", "Saturn", "Sonne"]

def make_feasts():
    our = date.today()
    kalendae = date(our.year, our.month, 1)
    revelationes = date(our.year, our.month, 8)
    idus = date(our.year, our.month, 15)
    terminaliae = date(our.year, our.month, 22)
    kalendae_next_month = kalendae + relativedelta(months=1)
    return {kalendae: 'Kalendae', revelationes: 'Revelationes', idus:'Idus', terminaliae: 'Terminaliae', kalendae_next_month:'Kalendae des Folgemonats'}


def get_last_next_feast(our,feasts):
    for date, name in feasts.items():
        feast = (name, abs((date-our).days))
        if date > our:
            return {'last': last_feast, 'next': feast}
        last_feast = feast

def it_is():
    our = date.today()
    feasts = collections.OrderedDict(sorted(make_feasts().items()))
    if our in feasts.keys():
        return "Heute sind die %s" % feasts[our]
    else:
        last_next = get_last_next_feast(our, feasts)
        message = "Es sind  %s Tag(e) bis zu den %s." % (last_next['next'][1], last_next['next'][0])
        message += " Seit den %s sind %s Tage vergangen." % (last_next['last'][0], last_next['last'][1])
        return message + "\n"

class Subscriptions:
    subscribers = dict()

    def add(self,jid):
        if str(JID(jid).full) not in self.subscribers:
            self.subscribers.update({str(JID(jid).full): None})

    def remove(self,jid):
        self.subscribers.pop(str(JID(jid).full))

    def __getattr__(self,name):
        return self.subscriber[name]

    def __setattr__(self,name,value):
        self.subscriber[name] = value

    def load(self, filename):
        with open(filename) as fp:
            self.subscribers = json.load(fp)

    def try_load(self,filename):
        try:
            self.load(filename)
        except FileNotFoundError:
            return

    def save(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self.subscribers,fp)






if __name__ == '__main__':
    
    
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=False)
        print("Done")
    else:
        print("Unable to connect.")
