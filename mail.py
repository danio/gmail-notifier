## mail.py - utilities for reading mail from gmail and formatting
## as HTML

# ======================================================================
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
# ======================================================================

import urllib
import feedparser

_URL = "https://mail.google.com/gmail/feed/atom"

class MyURLopener(urllib.FancyURLopener):
    def __init__(self, username, password):
        urllib.FancyURLopener.__init__(self)
        self.username = username
        self.password = password
        
    def prompt_user_passwd(self, host, realm):
        try:
            return self.username, self.password
        except:
            return None, None    

def get(url, opener):
    f = opener.open(url)
    feed = f.read()
    atom = feedparser.parse(feed)
    return atom
   
def getmail(url, username, password):
    # convert username and password to string type
    # so that urllib can handle them
    opener = MyURLopener(str(username), str(password))
    atom = get(url, opener)
    return atom.entries

if __name__ == "__main__":
    opener = urllib.FancyURLopener()
    atom = get(_URL, opener)
    for i in xrange(len(atom.entries)):
        print atom.entries[i].title + " " + atom.entries[i].author

