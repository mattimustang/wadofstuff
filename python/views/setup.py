from distutils.core import setup

import wadofstuff.django.views

README = open('README').read().strip() + "\n\n"
ChangeLog = \
    "What's new\n" + \
    "==========\n" + \
    "\n" + \
    open('ChangeLog').read().strip()
  
LONG_DESCRIPTION = README + ChangeLog

setup(
    name='wadofstuff-django-views',
    version=wadofstuff.django.views.__version__,
    description='Inlines support for Django generic views.',
    long_description=LONG_DESCRIPTION,
    author='Matthew Flanagan',
    author_email='mattimustang@gmail.com',
    url='http://code.google.com/p/wadofstuff/',
    download_url='http://wadofstuff.googlecode.com/files/wadofstuff-django-views-1.0.1.tar.gz',
    packages=(
        'wadofstuff',
        'wadofstuff.django',
        'wadofstuff.django.views',
    ),
    keywords="django views inlines",
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Framework :: Django',
    ),
)

