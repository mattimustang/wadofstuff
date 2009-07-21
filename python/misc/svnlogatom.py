#!/usr/bin/python
"""Convert output from svn log -v --xml to ATOM"""

from datetime import datetime
import urllib2
from xml.sax import parse
from xml.sax.handler import ContentHandler 
from xml.sax.saxutils import escape

URL='http://extjs.com/products/extjs/svnlog.xml'

class ExtHandler(ContentHandler):

    def __init__(self):
        self.paths = []
        self.msg = ''
        self.isMsg = False
        self.isAuthor = False
        self.isDate = False
        self.isPath = False

    def startElement(self, name, attrs):
        if name == 'logentry':
            self.revision = attrs.get('revision', "")
        elif name == 'msg':
            self.isMsg = True
        elif name == 'author':
            self.isAuthor = True
        elif name == 'date':
            self.isDate = True
        elif name == 'path':
            self.isPath = True
            self.paths.append([attrs.get('action', "")])
        return
            
    def characters(self, content):
        if self.isMsg:
            self.msg += content
        elif self.isAuthor:
            self.author = content
        elif self.isDate:
            self.date = content
        elif self.isPath:
            self.paths[-1].append(content)

    def endElement(self, name):
        if name == 'logentry':
            print "<entry>"
            print '<title type="text">%s</title>' % escape("%s: %s" % (self.revision, self.msg.replace('\n', ' ')))
            print "<id>%s</id>" % self.revision
            print "<updated>%s</updated>" % self.date
            print "<author><name>%s</name></author>" % self.author
            print '<summary type="html" xml:space="preserve">%s</summary>' % escape('<p>%s</p><p>Files:<ul>%s</ul></p>' % (self.msg.replace('\n', '<br/>'), ''.join(["<li>%s %s</li>" % (a,p) for a,p in self.paths])))
            print "</entry>"
            self.paths = []
            self.msg = ''
        elif name == 'msg':
            self.isMsg = False
        elif name == 'author':
            self.isAuthor = False
        elif name == 'date':
            self.isDate = False
        elif name == 'path':
            self.isPath = False

if __name__ == '__main__':
    now = datetime.utcnow()
    now = "%sT%s:%s:%sZ" % (now.date(), now.hour, now.minute, now.second)
    print """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>EXTJS SVN Commit Log</title>
<link href="http://extjs.com/products/extjs/commitlog.php" />
<updated>%s</updated>
<generator uri="svnlogatom.py" version="1.0">SVN Log to Atom</generator>
""" % now
    parse(urllib2.urlopen(URL), ExtHandler())
    print "</feed>"
