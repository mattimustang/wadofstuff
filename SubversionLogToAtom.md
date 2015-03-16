

# Introduction #

A simple Python module and script to convert the output from `svn log -v --xml` to Atom so that it can be consumed by a feed reader such as Google Reader.

# Download #

The script can be obtained from http://code.google.com/p/wadofstuff/source/browse/trunk/python/misc/svnlogatom.py.

# Usage #

The `svnlogatom.py` script takes one required argument and two optional arguments.

The script uses Python's `urllib2` to access the Subversion log file so it may reside on a local filesystem:

```
$ svnlogatom.py file:///path/to/svnlog.xml
```

or a remote one:

```
$ svnlogatom.py http://www.example.com/svnlog.xml
```

The optional arguments are the Atom Feed _title_ and _link_:

```
$ svnlogatom.py file:///path/to/svnlog.xml "My OpenSource Project" http://www.example.com/myproj
```

If these arguments are omitted then the svn log xml location is used.