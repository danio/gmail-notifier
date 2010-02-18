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

def feedtohtml(atom):
    html = "<table>" + "\n"
    html += "<tr><th>Subject</th><th>Sender</th></tr>"
    for i in xrange(len(atom.entries)):
        html += "<tr><td>" + atom.entries[i].title + "</td>"
        html += "<td>" + atom.entries[i].author + "</td></tr>\n"
    html += "</table>"
    return html
    
def getmail(url, username, password):
    try:
        # convert username and password to string type
        # so that urllib can handle them
        opener = MyURLopener(str(username), str(password))
        print "get"
        atom = get(url, opener)
    except:
        return "Failed to open " + _URL + ".<p>Check your username and password."
    return feedtohtml(atom)   

if __name__ == "__main__":
    opener = urllib.FancyURLopener()
    atom = get(_URL, opener)
    print feedtohtml(atom)

