"""Wad of Stuff Forms"""
from django import forms
from django.forms.models import BaseInlineFormSet

__all__ = ('RequireOneFormSet',)

class RequireOneFormSet(BaseInlineFormSet):
    """Require at least one form in the formset to be completed."""
    def clean(self):
        """Check that at least one form has been completed."""
        super(RequireOneFormSet, self).clean()
        for error in self.errors:
            if error:
                return
        completed = 0
        for cleaned_data in self.cleaned_data:
            # form has data and we aren't deleting it.
            if cleaned_data and not cleaned_data.get('DELETE', False):
                completed += 1

        if completed < 1:
            raise forms.ValidationError("At least one %s is required." %
                self.model._meta.object_name.lower())

# vim: ai ts=4 sts=4 et sw=4
