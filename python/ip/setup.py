from distutils.core import setup

from wadofstuff import ip

README = open('README').read().strip() + "\n\n"
ChangeLog = \
    "What's new\n" + \
    "==========\n" + \
    "\n" + \
    open('ChangeLog').read().strip()
  
LONG_DESCRIPTION = README + ChangeLog

setup(
    name='wadofstuff-ip',
    version=ip.__version__,
    description='IPv4 and IPv6 address summarization tool',
    long_description=LONG_DESCRIPTION,
    author='Matthew Flanagan',
    author_email='mattimustang@gmail.com',
    url='http://code.google.com/p/wadofstuff/',
    download_url='http://wadofstuff.googlecode.com/files/wadofstuff-ip-1.0.0.tar.gz',
    packages=(
        'wadofstuff',
        'wadofstuff.ip',
    ),
    requires=('IPy',),
    keywords="ipv4 ipv6 summarize",
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ),
)

