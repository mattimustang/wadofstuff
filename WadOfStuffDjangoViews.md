

# Requirements #

Django 1.0 or newer.

# Installation #

## From Source ##

Download wadofstuff-django-views from http://code.google.com/p/wadofstuff/downloads/list.

To install it, run the following command inside the unpacked source directory:

```
python setup.py install
```

## From PYPI ##

If you have the Python ```easy_install``` utility available, you can
also type the following to download and install in one step:

```
easy_install wadofstuff-django-views
```

Or if you're using ```pip```:

```
pip install wadofstuff-django-views
```

Or if you'd prefer you can simply place the included ```wadofstuff```
directory somewhere on your Python path, or symlink to it from
somewhere on your Python path; this is useful if you're working from a
Subversion checkout.

Note that this application requires Python 2.4 or later. You can obtain
Python from http://www.python.org/.


# Functions #

## wadofstuff.django.views.create\_object(..., inlines=None) ##
## wadofstuff.django.views.update\_object(..., inlines=None) ##

These functions are identical to the Django ones except for the addition of the
`inlines` argument. This argument consists of a list of dictionaries that will
be passed as arguments after the `parent_model` argument to
`inlineformset_factory(parent_model, ...)`.

For example, arguments to a generic view might typically look like:

```
crud_dict = {
    'model':Author
    'inlines':[{
        'model':Book,
        'extra':2,
        'form':BookForm,
    },{
        'model':Article,
    }],
    # ... other generic view arguments
}
```

would translate to calls to `inlineformset_factory()` like:

```
inlineformset_factory(Author, model=Book, extra=2, form=BookForm)
```

and
```
inlineformset_factory(Author, model=Article)
```

The view function will create a formset for each inline model and add them to
the template context. In the example above the context variables would be named
`book_formset` and `article_formset`.