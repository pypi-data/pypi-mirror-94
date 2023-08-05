"""function for assigning fields
"""

import datetime
import os
import warnings
import pandas as pd
import numpy as np
import pickle
import json
import uuid

import datajoint as dj
from datajoint.declare import match_type
from datajoint import FreeTable
from datajoint.table import lookup_class_name
from datajoint.utils import to_camel_case
from flask import url_for
from wtforms import BooleanField, SelectField, DateField, DateTimeField, \
    StringField, FloatField, IntegerField, FormField, \
    TextAreaField, FieldList, DecimalField, HiddenField
from wtforms.validators import InputRequired, Optional, NumberRange, \
    ValidationError, Length, UUID, URL, Email
from werkzeug.datastructures import FileStorage
from markupsafe import escape

from loris import config
from loris.utils import is_manuallookup
from loris.app.utils import name_lookup, datareader
from loris.app.forms import NONES
from loris.app.forms.formmixin import (
    ManualLookupForm, ParentFormField, DynamicFileField, DictField, ListField,
    ParentValidator, JsonSerializableValidator, AttachFileField,
    BlobFileField, Extension, TagListField, MetaHiddenField,
    ParentInputRequired, Always, LookupNameValidator, PutValidator,
    HtmlLabelSelectWidget, TagDictField
)
from loris.database.attributes import PrefixId


class DynamicField:
    """Choose the right wtf field for each attribute in a datajoint Table

    Parameters
    ----------
    table : class
        datajoint.Table subclass representing a table in the mySQL database.
    attribute : `dj.Attribute`
        attribute in table to create a field for.
    ignore_foreign_fields : bool
        whether to process foreign keys to create foreign field forms or
        simply normal fields.
    """

    def __init__(self, table, attribute, ignore_foreign_fields=False):

        self._table = table
        self._attribute = attribute
        self._foreign_table, self._aliased = self.get_foreign_table()
        self._ignore_foreign_fields = ignore_foreign_fields

        # set default values
        self.foreign_fields = {}

    @property
    def is_integer(self):
        # won't work with adapted types
        return match_type(self.type) == 'INTEGER'

    @property
    def is_uuid(self):
        return match_type(self.type) == 'UUID'

    @property
    def is_datelike(self):
        return match_type(self.type) == 'TEMPORAL'

    @property
    def ignore_foreign_fields(self):
        return self._ignore_foreign_fields

    @property
    def aliased(self):
        return self._aliased

    @property
    def table(self):
        return self._table

    @property
    def attribute(self):
        return self._attribute

    @property
    def attr(self):
        if isinstance(self._attribute, list):
            return self._attribute[0]
        else:
            return self._attribute

    @property
    def name(self):
        if isinstance(self._attribute, list):
            return '___'.join([attr.name for attr in self._attribute])
        return self.attr.name

    @property
    def names(self):
        if isinstance(self._attribute, list):
            return [attr.name for attr in self._attribute]
        return [self.attr.name]

    @property
    def in_key(self):
        return self.attr.in_key

    @property
    def nullable(self):
        return self.attr.nullable

    @property
    def comment(self):
        if isinstance(self._attribute, list):
            return ''
        return self.attr.comment

    @property
    def default(self):
        if isinstance(self._attribute, list):
            return None
        return self.attr.default

    # shouldn't be used if attribute is foreign_key
    @property
    def type(self):
        return self.attr.type

    @property
    def sql_type(self):
        return self.attr.sql_type

    @property
    def adapter(self):
        return self.attr.adapter

    @property
    def is_prefixid(self):
        return (
            match_type(self.type) == 'ADAPTED'
        ) and isinstance(self.adapter, PrefixId)

    @property
    def is_blob(self):
        return self.attr.is_blob

    @property
    def dependencies(self):
        """
        """

        if not (self.table.connection.dependencies):
            self.table.connection.dependencies.load()

        return self.table.connection.dependencies

    @property
    def is_foreign_key(self):
        """whether attribute is foreign key
        """
        return self.foreign_table is not None

    def get_foreign_table(self):
        """
        """
        aliased = None
        parents = self.dependencies.parents(self.table.full_table_name)
        for table_name, table_info in parents.items():
            # TODO check
            if set(self.names) == set(table_info['attr_map']):
                # deal with aliasing
                if table_info['aliased']:
                    aliased_parents = self.dependencies.parents(table_name)
                    # aliased parent should only be one
                    table_name = list(aliased_parents)[0]
                    aliased = table_info['attr_map']
                break
        else:
            return None, aliased

        return config.get_table(table_name), aliased

    @property
    def foreign_table(self):
        return self._foreign_table

    @property
    def singular(self):
        return (
            not isinstance(self._attribute, list)
            or len(self._attribute) == 1
        )

    @property
    def foreign_data(self):
        if self.aliased is None:
            data = self.foreign_table.proj().fetch()
        else:
            data = self.foreign_table.proj(**self.aliased).fetch()

        if self.singular:
            data = data[self.name]
            # sort values if integer
            # if self.is_integer:
            # always sort values
            data = np.sort(data)
        else:
            data = pd.DataFrame(
                data
            ).sort_values(self.names)[self.names].to_records(index=False)
        # elif:
        #     data = pd.DataFrame(data).
        return data

    @property
    def foreign_comment_data(self):
        if self.foreign_is_simple_manuallookup:
            return self.foreign_table.proj("comments").fetch()["comments"]
        else:
            return self.foreign_data

    @property
    def foreign_is_manuallookup(self):
        if not self.is_foreign_key:
            return False
        return (
            (
                self.foreign_table.full_table_name
                != config.user_table.full_table_name
            ) & (
                self.foreign_table.full_table_name
                != config.assigned_table.full_table_name
            )
        )
        # return True # TODO test is_manuallookup(self.foreign_table)

    @property
    def foreign_is_simple_manuallookup(self):
        if not self.is_foreign_key:
            return False
        else:
            return is_manuallookup(self.foreign_table)

    def create_field(self):
        """create field for dynamic form
        """

        field = self._create_field()

        if field is None:
            warnings.warn(
                f'No field generated for {self.name} of '
                f'type {self.type}'
            )

        return field

    def _create_field(self, attr_type=None, kwargs=None):
        """create field for dynamic form
        """

        if kwargs is None:
            kwargs = self.get_init_kwargs()

        if (
            self.is_foreign_key
            and not self.ignore_foreign_fields
            and self.foreign_is_manuallookup
        ):
            return self.create_manuallookup_field(kwargs)
        elif (
            self.is_foreign_key
            # and (len(self.foreign_data) <= config['fk_dropdown_limit'])
        ):
            return self.create_dropdown_field(kwargs)

        if attr_type is None:
            type = match_type(self.type)
            sql_type = self.sql_type
        else:
            sql_type = attr_type
            type = match_type(attr_type)

        if type == 'INTEGER':
            return self.integer_field(kwargs)
        elif type == 'DECIMAL':
            return self.decimal_field(kwargs)
        elif type == 'FLOAT':
            return self.float_field(kwargs)
        elif type == 'STRING':
            return self.string_field(kwargs, sql_type)
        elif type == 'ENUM':
            return self.enum_field(kwargs, sql_type)
        elif type == 'BOOL':
            return self.bool_field(kwargs)
        elif type == 'TEMPORAL':
            return self.temporal_field(kwargs, sql_type)
        elif type in ('INTERNAL_BLOB', 'EXTERNAL_BLOB'):
            return self.blob_field(kwargs)
        elif type in ('INTERNAL_ATTACH', 'EXTERNAL_ATTACH'):
            return self.attach_field(kwargs)
        elif type == 'FILEPATH':
            return self.filepath_field(kwargs)
        elif type == 'UUID':
            return self.uuid_field(kwargs)
        elif type == 'ADAPTED':
            return self.adapted_field(kwargs)

    def get_init_kwargs(self):
        """get initialization dictionary to pass to field class
        """

        kwargs = {}
        attr_name = self.name.replace('___', ', ').replace('_', ' ')
        if not self.is_foreign_key:
            kwargs['label'] = attr_name
        else:
            # add table url
            url_kwargs = dict(zip(
                ['schema', 'table', 'subtable'],
                name_lookup(self.foreign_table.full_table_name).split('.')
            ))
            if self.in_key:
                color = 'Crimson'
            elif self.nullable:
                color = 'DarkGray'
            else:
                color = 'Black'
            kwargs['label'] = (
                f'<a href="{url_for("table", **url_kwargs)}" '
                f'target="_blank">'
                f'<font color={color}>'
                f'{attr_name}'
                '</font>'
                '</a>'
            )
        if self.comment.strip():
            kwargs['description'] = self.comment.strip()
        elif not self.is_foreign_key:
            kwargs['description'] = self.name.replace('___', ', ').replace('_', ' ')

        nullable = self.nullable  # or self.default in NONES
        kwargs['render_kw'] = {
            'nullable': self.nullable,
            'primary_key': self.in_key
        }

        # ignore_foreign_fields assumes that a parent form is being created
        if nullable or (self.ignore_foreign_fields and self.in_key):
            kwargs['default'] = None
        else:
            kwargs['default'] = self.default

        if (
            (self.in_key or not nullable)
            and not self.ignore_foreign_fields
        ):
            # case of no pop up
            kwargs['validators'] = [InputRequired()]
        elif (self.in_key or not nullable) and self.ignore_foreign_fields:
            # case when foreign key pop up form
            kwargs['validators'] = [ParentInputRequired()]
        else:
            kwargs['validators'] = [Optional()]

        return kwargs

    def integer_field(self, kwargs):
        # auto increment integer primary keys
        kwargs['default'] = self._get_integer_default()
        return IntegerField(**kwargs)

    def _get_integer_default(self):
        # auto increment integer primary keys
        default = None
        if self.ignore_foreign_fields and self.in_key:
            pass
        elif len(self.table()) == 0:
            default = 1
        elif self.in_key and len(self.table.heading.primary_key) == 1:
            default = np.max(
                self.table.proj().fetch()[self.name]
            ) + 1
        return default

    def _get_prefixid_default(self):
        default = None
        if self.ignore_foreign_fields and self.in_key:
            pass
        elif len(self.table()) == 0:
            default = f'{self.adapter.prefix}1'
        elif self.in_key and len(self.table.heading.primary_key) == 1:
            default = self.table.proj().fetch()[self.name]
            default = pd.Series(
                default
            ).str[len(self.adapter.prefix):].astype(int).max() + 1
            default = f'{self.adapter.prefix}{default}'
        return default

    def float_field(self, kwargs):
        return FloatField(**kwargs)

    def decimal_field(self, kwargs):
        # implement rounding correctly and use DecimalField
        return FloatField(**kwargs)

    def string_field(self, kwargs, sql_type):
        """creates a string field
        """
        max_length = int(sql_type.split('(')[-1][:-1])

        if sql_type.startswith('varchar'):
            kwargs['validators'].append(Length(max=max_length))
        elif sql_type.startswith('char'):
            kwargs['validators'].append(Length(min=max_length, max=max_length))
        else:
            return

        if max_length >= config['textarea_startlength']:
            return TextAreaField(**kwargs)
        else:
            return StringField(**kwargs)

    def temporal_field(self, kwargs, sql_type):
        """date and datetime field
        """

        if sql_type in ('datetime', 'timestamp'):
            if not (self.ignore_foreign_fields and self.in_key):
                kwargs['default'] = datetime.datetime.today
            kwargs['label'] += '&emsp;<small>(Y/m/d H:M - e.g. 2020/01/01 11:11)</small>&emsp;'
            return DateTimeField(format='%Y/%m/%d %H:%M', **kwargs)
        elif sql_type == 'time':
            if not (self.ignore_foreign_fields and self.in_key):
                kwargs['default'] = datetime.datetime.today
            kwargs['label'] += '&emsp;<small>(H:M - e.g. 11:11)</small>&emsp;'
            return DateTimeField(format='%H:%M', **kwargs)
        elif sql_type == 'date':
            if not (self.ignore_foreign_fields and self.in_key):
                kwargs['default'] = datetime.date.today
            kwargs['label'] += '&emsp;<small>(Y/m/d - e.g. 2020/01/01)</small>&emsp;'
            return DateField(format='%Y/%m/%d', **kwargs)
        elif sql_type == 'year':
            if not (self.ignore_foreign_fields and self.in_key):
                kwargs['default'] = datetime.date.today
            kwargs['label'] += '&emsp;<small>(Y - e.g. 2020)</small>&emsp;'
            return DateField(format='%Y', **kwargs)

    def _get_temporal_default(self):
        if self.sql_type in ('year', 'date'):
            if not (self.ignore_foreign_fields and self.in_key):
                return datetime.date.today
        elif not (self.ignore_foreign_fields and self.in_key):
            return datetime.datetime.today

    def enum_field(self, kwargs, sql_type):
        """create field for enum
        """
        choices = sql_type[sql_type.find('(')+1:sql_type.rfind(')')].split(',')
        choices = [ele.strip().strip('"').strip("'") for ele in choices]
        if self.nullable:
            choices = ['NULL'] + choices
        kwargs['choices'] = [(ele, ele) for ele in choices]
        return SelectField(**kwargs)

    def bool_field(self, kwargs):
        if kwargs['default'] is None:
            kwargs['default'] = False
        elif kwargs['default']:
            kwargs['default'] = True
        else:
            kwargs['default'] = False
        # input always optional
        kwargs['validators'][0] = Optional()
        return BooleanField(**kwargs)

    def blob_field(self, kwargs):
        kwargs['validators'] = [Optional()]  # TODO fix for editing
        kwargs['validators'].append(Extension())
        return BlobFileField(**kwargs)

    def attach_field(self, kwargs):
        kwargs['validators'] = [Optional()]  # TODO fix for editing
        kwargs['validators'].append(Extension(config['attach_extensions']))
        return AttachFileField(**kwargs)

    def filepath_field(self, kwargs):
        # TODO implement
        # kwargs['validators'].append(FilePath())
        return

    def uuid_field(self, kwargs):
        kwargs['validators'].append(Length(36, 36))
        kwargs['validators'].append(UUID())
        kwargs['default'] = str(uuid.uuid4())
        return StringField(**kwargs)

    def adapted_field(self, kwargs):
        """creates an adapted field type
        """

        try:
            attr_type = self.adapter.attribute_type
        except NotImplementedError:
            attr_type = self.sql_type

        attr_type_name = self.type.strip('<>')
        adapter = config['custom_attributes'].get(attr_type_name, None)

        if self.is_prefixid:
            kwargs['default'] = self._get_prefixid_default()

        if adapter is None:
            pass
        elif attr_type_name == 'liststring':
            kwargs['validators'].append(
                JsonSerializableValidator(list, adapter.put))
            return ListField(**kwargs)
        elif attr_type_name == 'dictstring':
            kwargs['validators'].append(
                JsonSerializableValidator(dict, adapter.put))
            return DictField(**kwargs)
        elif attr_type_name == 'tags':
            return TagListField(**kwargs)
        elif attr_type_name == 'dicttags':
            return TagDictField(**kwargs)
        elif attr_type_name == 'link':
            kwargs['validators'].append(URL(False))
        elif attr_type_name == 'email':
            kwargs['validators'].append(Email())
        elif attr_type_name == 'lookupname':
            kwargs['validators'].append(LookupNameValidator())
        else:
            kwargs['validators'].append(PutValidator(adapter.put))

        return self._create_field(attr_type, kwargs)

    def create_manuallookup_field(self, kwargs):
        """create a manual lookup field form.
        """

        kwargs['id'] = 'existing_entries'
        if self.aliased is None:
            kwargs['validators'].insert(0, ParentValidator(self.names))
        else:
            kwargs['validators'].insert(
                0,
                ParentValidator([self.aliased[name] for name in self.names])
            )

        # dynamically create form
        class FkForm(ManualLookupForm):
            parent_table_name = to_camel_case(self.foreign_table.table_name)
            existing_entries = self.create_dropdown_field(kwargs)

        for name, attr in self.foreign_table.heading.attributes.items():
            dynamicfield = DynamicField(self.foreign_table, attr, True)
            # create field
            field = dynamicfield.create_field()
            if field is not None:
                setattr(
                    FkForm,
                    name,
                    field
                )
                # keep track of dynamic fields
                self.foreign_fields[name] = dynamicfield

        return ParentFormField(FkForm)

    def create_dropdown_field(self, kwargs):
        """a simple drowndown field for foreign keys
        """

        choices = self.get_foreign_choices()
        if self.nullable:
            kwargs['default'] = 'NULL'

        if choices:
            kwargs['choices'] = choices
            kwargs['widget'] = HtmlLabelSelectWidget()
            return SelectField(**kwargs)
        else:
            kwargs['label'] += ' -- <font color="red">MISSING ENTRIES IN PARENT TABLE!</font>'
            kwargs['validators'].append(Always())
            return MetaHiddenField(**kwargs)

    def get_foreign_choices(self):
        if self.foreign_is_simple_manuallookup:
            choices = [
                (str(ele), (str(ele), str(comment)))
                if comment is not None
                else
                (str(ele), str(ele))
                for ele, comment
                in zip(self.foreign_data, self.foreign_comment_data)
            ]
        else:
            choices = [
                (str(ele), str(ele))
                for ele in self.foreign_data
            ]
        choices = sorted(choices)
        if self.nullable:
            choices = [('NULL', 'NULL')] + choices
        if self.foreign_is_manuallookup and not self.ignore_foreign_fields:
            choices += [('<new>', '<add new entry>')]

        return choices

    def format_value(self, value):
        """format value
        """

        if self.foreign_is_manuallookup:
            if value['existing_entries'] == '<new>':
                value.pop('existing_entries')
                try:
                    self.foreign_table.insert1(
                        self.foreign_table_format_value(value)
                    )
                except dj.DataJointError as e:
                    raise dj.DataJointError(
                        "An error occured while inserting into parent table"
                        f" {self.foreign_table.full_table_name}: {e}"
                    )
                if self.aliased is None:
                    return {name: value[name] for name in self.names}
                else:
                    return {name: value[self.aliased[name]]
                            for name in self.names}
            elif self.singular:
                return {
                    self.name: value['existing_entries']
                }
            else:
                values = value['existing_entries'].strip('()').split(', ')
                # strip any quotes
                values = [ele.strip().strip('"').strip("'") for ele in values]
                return dict(zip(self.names, values))

        if self.is_blob:
            value = self._process_blob_value(value)

        # return value
        return {self.name: value}

    @staticmethod
    def _process_blob_value(value):
        """process blobs by loading files
        """

        if value in NONES:
            value = None
        else:
            value = datareader(value)

        return value

    def foreign_table_format_value(self, value):
        """process foreign table values before insertion
        """
        for name, attr in self.foreign_table.heading.attributes.items():
            if attr.is_blob and name in value:
                value[name] = self._process_blob_value(value[name])
        return value

    def prepare_populate(self, value):
        """format value for populating form
        """

        if self.foreign_is_manuallookup:
            value = {
                'existing_entries': str(value)
            }

        if self.is_blob and value is not None:
            # create filepath
            # TODO - not functional atm
            filepath = os.path.join(
                config['tmp_folder'],
                str(uuid.uuid4()) + '.pkl'
            )
            with open(filepath, 'wb') as f:
                pickle.dump(value, f, protocol=pickle.HIGHEST_PROTOCOL)

            return filepath

        return value

    def update_field(self, form):

        if self.foreign_is_manuallookup and not self.ignore_foreign_fields:
            formfield = getattr(form, self.name)
            formfield.existing_entries.choices = self.get_foreign_choices()

            # update fields in parent form
            for name, foreign_dynamicfield in self.foreign_fields.items():
                foreign_dynamicfield.update_field(formfield)

            # update field if necessary
            if self.singular:
                self._update_field(formfield)

        elif self.is_foreign_key:
            field = getattr(form, self.name)
            field.choices = self.get_foreign_choices()

        else:
            self._update_field(form)

    def _update_field(self, form):

        if self.is_uuid:
            field = getattr(form, self.name)
            field.default = str(uuid.uuid4())
        if self.is_integer:
            field = getattr(form, self.name)
            field.default = self._get_integer_default()
        if self.is_datelike:
            field = getattr(form, self.name)
            field.default = self._get_temporal_default()
        if self.is_prefixid:
            field = getattr(form, self.name)
            field.default = self._get_prefixid_default()
