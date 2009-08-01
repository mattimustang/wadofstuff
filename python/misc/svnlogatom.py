#!/usr/bin/python
"""Convert output from svn log -v --xml to ATOM"""

from datetime import datetime
import sys
import urllib2
from xml.sax import make_parser, SAXParseException
from xml.sax.handler import ContentHandler 
from xml.sax.saxutils import escape

__version__ = '1.0'

class SvnLogHandler(ContentHandler):
    """Convert Subversion Commit Log XML to Atom."""
    def __init__(self):
        """Initialise instance variables."""
        self._content = ''
        self.paths = []
        self.msg = ''
        self.author = ''
        self.date = ''
        self.revision = ''
        self.is_msg = False
        self.is_author = False
        self.is_date = False
        self.is_path = False
        ContentHandler.__init__(self)

    @property
    def content(self):
        """The generated Atom content."""
        return self._content

    def startElement(self, name, attrs):
        """Set flags depending on which Subversion log element is parsed."""
        if name == 'logentry':
            self.revision = attrs.get('revision', "")
        elif name == 'msg':
            self.is_msg = True
        elif name == 'author':
            self.is_author = True
        elif name == 'date':
            self.is_date = True
        elif name == 'path':
            self.is_path = True
            self.paths.append([attrs.get('action', "")])
        return
            
    def characters(self, content):
        """Extract the content of the element."""
        if self.is_msg:
            self.msg += content
        elif self.is_author:
            self.author = content
        elif self.is_date:
            self.date = content
        elif self.is_path:
            self.paths[-1].append(content)

    def endElement(self, name):
        """Reset all the element flags and generate Atom XML if we have
        reached the end of a logentry."""
        if name == 'logentry':
            self._content += "<entry>"
            _title = escape("%s: %s" % (self.revision,
                self.msg.replace('\n', ' ')))
            self._content += '<title type="text">%s</title>' % _title
            self._content += "<id>%s</id>" % self.revision
            self._content += "<updated>%s</updated>" % self.date
            self._content += "<author><name>%s</name></author>" % self.author
            _summary = escape('<p>%s</p><p>Files:<ul>%s</ul></p>' % 
                (self.msg.replace('\n', '<br/>'),
                ''.join(["<li>%s %s</li>" % (a,p) for a,p in self.paths])))
            self._content += ('<summary type="html" xml:space="preserve">%s'
                '</summary>' % _summary)
            self._content += "</entry>"
            self.paths = []
            self.msg = ''
        elif name == 'msg':
            self.is_msg = False
        elif name == 'author':
            self.is_author = False
        elif name == 'date':
            self.is_date = False
        elif name == 'path':
            self.is_path = False

def generate(file_object, title, link):
    """Generate the Atom xml."""
    now = datetime.utcnow()
    now = "%sT%s:%s:%sZ" % (now.date(), now.hour, now.minute, now.second)
    header = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
<title>%s</title>
<link href="%s" />
<updated>%s</updated>
<generator uri="svnlogatom.py" version="%s">SVN Log to Atom</generator>
""" % (title, link, now, __version__)
    footer = "</feed>"
    parser = make_parser()
    handler = SvnLogHandler()
    parser.setContentHandler(handler)
    try:
        parser.parse(file_object)
    except SAXParseException, err:
        sys.stderr.write("%s\n" % err)
        sys.exit(1)
    content = parser.getContentHandler().content
    return "%s%s%s" % (header, content, footer)

if __name__ == '__main__':
    __title = ''
    __link = ''
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s uri [title] [link]\n" % sys.argv[0])
        sys.exit(2)

    try:
        __file_obj = urllib2.urlopen(sys.argv[1])
    except Exception, __err:
        sys.stderr.write("%s\n" % __err)
        sys.exit(2)

    try:
        __title = sys.argv[2]
    except IndexError:
        __title = sys.argv[1]
    try:
        __link = sys.argv[3]
    except IndexError:
        __link = sys.argv[1]
    print generate(__file_obj, __title, __link)
