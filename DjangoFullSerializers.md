

# Introduction #

The wadofstuff.django.serializers python module extends [Django's built-in serializers](http://docs.djangoproject.com/en/dev/topics/serialization/), adding 3 new capabilities inspired by the Ruby on Rails [JSON serializer](http://dev.rubyonrails.org/browser/trunk/activerecord/lib/active_record/serializers/json_serializer.rb). These parameters allow the developer more control over how their models are serialized. The additional capabilities are:

  * excludes - a list of fields to be excluded from serialization. The excludes list takes precedence over the fields argument.

  * extras - a list of non-model field properties or callables to be serialized.

  * relations - a list or dictionary of model related fields to be followed and serialized.

# Serialization Formats #

The module currently support serializing to JSON and Python only.

# Source #

The latest stable release for the serialization module can be obtained by:

  * Running `easy_install wadofstuff-django-serializers`

  * Downloading [Wad of Stuff Django Serializers](http://wadofstuff.googlecode.com/files/wadofstuff-django-serializers-1.1.0.tar.gz)

The latest development source can be obtained here:

  * [Wad of Stuff Django Serializers source](http://wadofstuff.googlecode.com/svn/trunk/python/serializers)

# Examples #

## Project Settings ##

You must add the following to your project's `settings.py` to be able to use the JSON serializer.

```
SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}
```

## Backwards Compatibility ##

The Wad of Stuff serializers are 100% compatible with the Django serializers when serializing a model. When deserializing a data stream the the `Deserializer` class currently only works with serialized data returned by the standard Django serializers.

```
>>> from django.contrib.auth.models import Group
>>> from django.core import serializers
>>> print serializers.serialize('json', Group.objects.all(), indent=4)
[
    {
        "pk": 2,
        "model": "auth.group",
        "fields": {
            "name": "session",
            "permissions": [
                19
            ]
        }
    }
]
```

## Excludes ##

```
>>> print serializers.serialize('json', Group.objects.all(), indent=4, excludes=('permissions',))
[
    {
        "pk": 2,
        "model": "auth.group",
        "fields": {
            "name": "session"
        }
    }
]
```

## Extras ##

The `extras` option allows the developer to serialize properties of a model that are not fields. These properties may be almost any standard python attribute or method. The only limitation being that you may only serialize methods that do not require any arguments.

For demonstration purposes in this example I monkey patch the `Group` model to have a `get_absolute_url()` method.

```
>>> def get_absolute_url(self):
...     return u'/group/%s' % self.name
...
>>> Group.get_absolute_url = get_absolute_url
>>> print serializers.serialize('json', Group.objects.all(), indent=4, extras=('__unicode__','get_absolute_url'))
[
    {
        "pk": 2,
        "model": "auth.group",
        "extras": {
            "get_absolute_url": "/group/session",
            "__unicode__": "session"
        },
        "fields": {
            "name": "session",
            "permissions": [
                19
            ]
        }
    }
]
```

## Relations ##

The Wad of Stuff serializers allow you to follow related fields of a model to any depth you wish and serialize those as well. This is why it is considered a "full serializer" as opposed to Django's built-in serializers that only return the related fields primary key value.

When using the `relations` argument to the serializer you may specify either a list of fields to be serialized or a dictionary of key/value pairs. The dictionary keys are the field names of the related fields to be serialized and the values are the arguments to pass to the serializer when processing that field.

```
>>> print serializers.serialize('json', Group.objects.all(), indent=4, relations=('permissions',))
[
    {
        "pk": 2,
        "model": "auth.group",
        "fields": {
            "name": "session",
            "permissions": [
                {
                    "pk": 19,
                    "model": "auth.permission",
                    "fields": {
                        "codename": "add_session",
                        "name": "Can add session",
                        "content_type": 7
                    }
                }
            ]
        }
    }
]
```

### Only serializing a particular field of a relation ###

```
>>> print serializers.serialize('json', Group.objects.all(), indent=4, relations={'permissions':{'fields':('codename',)}})
[
    {
        "pk": 2,
        "model": "auth.group",
        "fields": {
            "name": "session",
            "permissions": [
                {
                    "pk": 19,
                    "model": "auth.permission",
                    "fields": {
                        "codename": "add_session"
                    }
                }
            ]
        }
    }
]
```

### Serializing a relation of a relation ###

```
>>> print serializers.serialize('json', Group.objects.all(), indent=4, relations={'permissions':{'relations':('content_type',)}})
[
    {
        "pk": 2,
        "model": "auth.group",
        "fields": {
            "name": "session",
            "permissions": [
                {
                    "pk": 19,
                    "model": "auth.permission",
                    "fields": {
                        "codename": "add_session",
                        "name": "Can add session",
                        "content_type": {
                            "pk": 7,
                            "model": "contenttypes.contenttype",
                            "fields": {
                                "model": "session",
                                "name": "session",
                                "app_label": "sessions"
                            }
                        }
                    }
                }
            ]
        }
    }
]
```

### Excluding a field from a relation of a relation ###

```
>>> print serializers.serialize('json', Group.objects.all(), indent=4, relations={'permissions':{'relations':{'content_type':{'excludes':('app_label',)}}}})
[
    {
        "pk": 2,
        "model": "auth.group",
        "fields": {
            "name": "session",
            "permissions": [
                {
                    "pk": 19,
                    "model": "auth.permission",
                    "fields": {
                        "codename": "add_session",
                        "name": "Can add session",
                        "content_type": {
                            "pk": 7,
                            "model": "contenttypes.contenttype",
                            "fields": {
                                "model": "session",
                                "name": "session"
                            }
                        }
                    }
                }
            ]
        }
    }
]
```