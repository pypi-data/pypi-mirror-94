"""Wtf Forms
"""

import os
import numpy as np
import json
import re
import warnings

from wtforms import FieldList, FormField, BooleanField, StringField, \
    TextAreaField, SelectField
from wtforms.widgets import HiddenInput
from wtforms import Form as NoCsrfForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, Optional, NumberRange, \
    ValidationError, Length, UUID, URL, Email, StopValidation
from wtforms.widgets import Select
from wtforms.widgets import html_params
from markupsafe import Markup, escape
from wtforms.compat import text_type

from loris import config
from loris.app.forms import NONES


class HtmlLabelSelectWidget(Select):

    @classmethod
    def render_option(cls, value, label, selected, **kwargs):
        if value is True:
            # Handle the special case of a 'True' value.
            value = text_type(value)

        if isinstance(label, (tuple, list)):
            comment = "(" + (
                label[1]
                if len(label[1]) < 52
                else label[1][:50] + '...'
            ) + ")"
            label = (
                f'{escape(label[0])}  '
                f'&emsp;<small>{escape(comment)}</small>')
            options = dict(kwargs, value=value, title=comment)
        else:
            label = escape(label)
            options = dict(kwargs, value=value)
        if selected:
            options["selected"] = True
        return Markup(
            f"<option {html_params(**options)}>{label}</option>"
        )


class MetaHiddenField(BooleanField):
    widget = HiddenInput()


class TagListField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(
        self, label='', validators=None, remove_duplicates=True,
        to_lowercase=True, separator=',', **kwargs
    ):
        """
        Construct a new field.

        Parameters
        ----------
        label: The label of the field.
        validators: A sequence of validators to call when validate is called.
        remove_duplicates: Remove duplicates in a case insensitive manner.
        to_lowercase: Cast all values to lowercase.
        separator: The separator that splits the individual tags.
        """
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return u'{} '.format(self.separator).join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [
                x.strip()
                for x in valuelist[0].split(self.separator)
                if x.strip()
            ]
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data]
            if not self.data:
                self.data = None

    @classmethod
    def _remove_duplicates(cls, seq):
        """
        Remove duplicates in a case insensitive,
        but case preserving manner
        """
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class TagDictField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(
        self, label='', validators=None,
        key_separator='=', separator=',', **kwargs
    ):
        """
        Construct a new field.

        Parameters
        ----------
        label: The label of the field.
        validators: A sequence of validators to call when validate is called.
        key_separator : The separator between key and value.
        separator: The separator that splits the individual tags.
        """
        super(TagDictField, self).__init__(label, validators, **kwargs)
        self.key_separator = key_separator
        self.separator = separator
        self.data = dict()

    def _value(self):
        if self.data:
            return u'{} '.format(self.separator).join([
                f"{key}{self.key_separator}{value}"
                for key, value in self.data.items()
            ])
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = dict([
                [ele.strip() for ele in x.strip().split(self.key_separator)]
                for x in valuelist[0].split(self.separator)
                if x.strip() and (self.key_separator in x.strip())
            ])
            if not self.data:
                self.data = None


class EvalJsonField:

    startswith = None
    endswith = None

    def _value(self):
        if self.data not in NONES:
            return json.dumps(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            data = valuelist[0]
            if data in NONES:
                self.data = None
            else:
                if (
                    not data.startswith(self.startswith)
                    or not data.endswith(self.endswith)
                ):
                    data = f'{self.startswith}{data}{self.endswith}'
                self.data = json.loads(data)


class ListField(EvalJsonField, StringField):
    startswith = '['
    endswith = ']'


class DictField(EvalJsonField, StringField):
    startswith = '{'
    endswith = '}'


class DictTextArea(EvalJsonField, TextAreaField):
    startswith = '{'
    endswith = '}'


class RestrictionField(StringField):

    def evaluate(self, data):
        if data in NONES:
            return False
        elif data.startswith('['):
            return True
        elif data.startswith('{'):
            return True
        else:
            return False

    def _value(self):
        if self.data in NONES:
            return ''
        elif isinstance(self.data, str):
            return self.data
        else:
            return json.dumps(self.data)

    def process_formdata(self, valuelist):
        if valuelist:
            data = valuelist[0]
            if data in NONES:
                self.data = None
            elif self.evaluate(data):
                self.data = json.loads(data)
            else:
                self.data = data


class DynamicFileField(FileField):
    pass  # TODO


class CamelCaseValidator:

    def __init__(self, name='table name'):

        self.name = name

    def __call__(self, form, field):

        if not re.match(r'[A-Z][a-zA-Z0-9]*', field.data):
            raise ValidationError(
                f'{self.name} must be alphanumeric in CamelCase, '
                'begin with a capital letter.'
            )


class Extension:
    """Extension Validator
    """

    def __init__(self, ext=config['extensions']):
        self.ext = ext

    def __call__(self, form, field):
        filename = field.data.filename
        if not filename:
            return
        extension = os.path.splitext(filename)[-1].strip('.')
        if extension.lower() not in self.ext:
            raise ValidationError(
                f"File {filename} is not of extension: {self.ext}, "
                f"but extension {extension}."
            )


class FilePath:

    def __call__(self, form, field):

        data = field.data
        if not os.path.exists(data):
            raise ValidationError(
                f'Filepath {data} does not exist.'
            )


class LookupNameValidator:

    def __call__(self, form, field):

        data = field.data

        if data in NONES:
            return

        if isinstance(data, str):
            data = data.strip().lower()
            if not data.isidentifier():
                raise ValidationError(
                    f"lookup name '{data}' is not an identifier; "
                    "it contains characters besides alphanumeric and/or "
                    "an underscore."
                )
        else:
            raise ValidationError(
                'Lookup Name must be of string type.'
            )


class ParentInputRequired(Optional):

    def __call__(self, form, field):
        """only required if <new> set
        """

        try:
            existing = getattr(form, 'existing_entries').data
        except AttributeError:
            existing = '<new>'

        if existing == '<new>':
            if field.data in NONES:
                raise ValidationError('Data missing!')

        super().__call__(form, field)


class Always:

    def __call__(self, form, field):
        try:
            existing = getattr(form, 'existing_entries').data
        except AttributeError:
            existing = '<new>'

        if existing == '<new>':
            raise ValidationError("Data completely missing!")


class ParentValidator:

    def __init__(self, primary_key):
        self.primary_key = primary_key

    def __call__(self, form, field):
        """
        """

        data = tuple([getattr(form, key).data for key in self.primary_key])

        if field.data == '<new>':
            if any(idata in NONES for idata in data):
                raise ValidationError(
                    'Must specify new foreign primary key '
                    'if <add new entry> is selected.'
                )
            if str(data) in [ele for ele, ele in field.choices]:
                raise ValidationError(
                    f'Entry {data} already exists in parent table.'
                )

        else:
            if any(idata not in NONES for idata in data):
                raise ValidationError(
                    'If specifying new foreign primary key '
                    'need to set select field to <add new entry>'
                )


class PutValidator:

    def __init__(self, put_test=None):
        self.put_test = put_test

    def __call__(self, form, field):

        data = field.data

        if self.put_test is not None:
            try:
                self.put_test(data)
            except Exception as e:
                raise ValidationError(
                    f'Data did not pass put test: {e}'
                )


class JsonSerializableValidator:

    def __init__(self, is_instance=None, put_test=None):
        self.is_instance = is_instance
        self.put_test = put_test

    def __call__(self, form, field):

        data = field.data

        if data in NONES:
            return

        if not isinstance(data, str):
            if (
                self.is_instance is not None
                and
                not isinstance(data, self.is_instance)
            ):
                raise ValidationError(
                    f'Json Data is not correct type {self.is_instance}, '
                    f'but is {type(data)}'
                )
        else:
            try:
                data = json.loads(data)
                if self.is_instance is not None:
                    assert isinstance(data, self.is_instance), (
                        f'Json Data is not correct type {self.is_instance}, '
                        f'but is {type(data)}'
                    )
            except Exception as e:
                raise ValidationError(
                    f'Data is not a json-serializable: {e}'
                )

        if self.put_test is not None:
            try:
                self.put_test(data)
            except Exception as e:
                raise ValidationError(
                    f'Data did not pass put test: {e}'
                )


class OptionalJsonSerializableValidator(JsonSerializableValidator):

    def __call__(self, form, field):
        if not isinstance(field.data, str):
            super().__call__(form, field)


class BlobFileField(DynamicFileField):
    pass


class AttachFileField(DynamicFileField):
    pass


class FormMixin:
    hidden_entries = None

    def populate_form(self, formatted_dict):
        """populate form from formatted_dict

        Parameters
        ----------
        formatted_dict : dict
            dictionary as formatted by get_formatted method.
        readonly : iterable
            field ids that are readonly.
        """
        if not isinstance(formatted_dict, dict):
            warnings.warn(
                "Formatted dictionary is not of type `dict`, "
                f"but of type `{type(formatted_dict)}`"
            )
            return self

        for field in self:
            key = field.short_name

            if key in formatted_dict:
                data = formatted_dict[key]

                if data is None:
                    continue

                elif isinstance(field, FieldList):
                    while len(field) > 1:
                        field.pop_entry()

                    subfield = field[0]

                    if isinstance(subfield, FormField):
                        for idata in data:
                            sanitized_data = subfield.populate_form(idata).data
                            field.append_entry(sanitized_data)

                    else:
                        for idata in data:
                            field.append_entry(idata)

                elif isinstance(field, FormField):
                    field.populate_form(data)

                else:
                    field.process_data(data)

        return self

    def rm_hidden_entries(self):
        """removes hidden entries in form to allow for dynamic lists
        """

        self.hidden_entries = {}
        self.subhidden_entries = []

        for field in self:

            if isinstance(field, FormField):
                field.rm_hidden_entries()
                self.subhidden_entries.append(field)

            elif isinstance(field, FieldList):

                hidden_entry = field.entries.pop(0)
                self.hidden_entries[field] = hidden_entry

                for subfield in field:
                    # check if subfield is formfield and pop entry
                    if isinstance(subfield, FormField):
                        subfield.rm_hidden_entries()
                        self.subhidden_entries.append(subfield)

    def append_hidden_entries(self):
        """reinsert hidden entries in form to allow for dynamiv lists
        """

        if self.hidden_entries is None:
            pass

        else:
            for subfield in self.subhidden_entries:
                subfield.append_hidden_entries()

            for field, hidden_entry in self.hidden_entries.items():

                field.entries.insert(0, hidden_entry)

            self.hidden_entries = None

    @staticmethod
    def get_field_data(field):

        def _get_field_data(field, nan_return):

            if field.data in NONES:
                return nan_return

            if isinstance(field, FileField):
                filename = secure_filename(field.data.filename)
                if filename in NONES:
                    return nan_return
                filepath = os.path.join(config['tmp_folder'], filename)
                field.data.save(filepath)
                return filepath

            return field.data

        if isinstance(field, BooleanField):
            return _get_field_data(field, False)
        else:
            return _get_field_data(field, None)

    def get_formatted(self):
        """get data from form and reformat for
        execution and saving
        """
        formatted_dict = {}
        for field in self:

            key = field.short_name

            if key == 'csrf_token':
                continue

            elif isinstance(field, FieldList):
                formatted_dict[key] = []

                for subfield in field:
                    if isinstance(subfield, FormField):
                        formatted_dict[key].append(subfield.get_formatted())

                    else:
                        formatted_dict[key].append(
                            self.get_field_data(subfield))

                # No Nones are allowed in a list, they will be removed
                # or the key will be set to None
                are_None = [value is None for value in formatted_dict[key]]

                if np.all(are_None):
                    formatted_dict[key] = None

                else:
                    formatted_dict[key] = [
                        value
                        for value in formatted_dict[key]
                        if value is not None]

            elif isinstance(field, FormField):
                formatted_dict[key] = field.get_formatted()

            else:
                formatted_dict[key] = self.get_field_data(field)
        return formatted_dict


class ManualLookupForm(NoCsrfForm, FormMixin):
    """parent class for manual lookup forms for instance checking.
    """
    pass


class ParentFormField(FormField):
    """FormField for a parent class for instance checking.
    """
    pass
