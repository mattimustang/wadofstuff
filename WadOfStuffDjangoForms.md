

# Requirements #

Django 1.0 or newer.

# Installation #

## From Source ##

Download wadofstuff-django-forms from http://code.google.com/p/wadofstuff/downloads/list.

To install it, run the following command inside the unpacked source directory:

```
python setup.py install
```

## From PYPI ##

If you have the Python ```easy_install``` utility available, you can
also type the following to download and install in one step:

```
easy_install wadofstuff-django-forms
```

Or if you're using ```pip```:

```
pip install wadofstuff-django-forms
```

Or if you'd prefer you can simply place the included ```wadofstuff```
directory somewhere on your Python path, or symlink to it from
somewhere on your Python path; this is useful if you're working from a
Subversion checkout.

Note that this application requires Python 2.4 or later. You can obtain
Python from http://www.python.org/.

# Functions #

## wadofstuff.django.forms.security\_hash(request, form, exclude=None, `*`args) ##

Calculates a security hash for the given Form/FormSet instance.

This creates a list of the form field names/values in a deterministic
order, pickles the result with the SECRET\_KEY setting, then takes an md5
hash of that.

Allows a list of form fields to be excluded from the hash calculation. This
is useful form fields that may have their values set programmatically.

# Classes #

## wadofstuff.django.forms.BoundFormWizard ##

A subclass of Django's FormWizard that adds the following functionality:

  * Renders `previous_fields` as a list of bound form fields in the template context rather than as raw html.
  * Can handle FormSets.

The usage of this class is identical to that documented at
http://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-wizard/ with
the exception that when rendering `previous_fields` you should change your
wizard step templates from:

```
    <input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />
    {{ previous_fields|safe }}
```

to:

```
    <input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />
    {% for f in previous_fields %}{{ f.as_hidden }}{% endfor %}
```

## wadofstuff.django.forms.RequireOneFormSet ##

A subclass of Django's `BaseInlineFormSet` that requires at least one form in
the formset to be completed.

Use this class as the `formset` argument to `inlineformset_factory()`.

When the formset is validated and it does not contain one or more entries, then
a `ValidationError` is raised which gets put into `formset.non_form_errors`. You
will need to check this in your templates if you wish to display the error
message to your users.