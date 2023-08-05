"""utils functions for autoscripting
"""

from ast import literal_eval
import numpy as np
import json
import pickle
import pandas as pd


def json_reader(value):
    """read json file fields
    """
    if value is None:
        return

    with open(value, 'r') as f:
        value = json.load(f)

    return value


def array_reader(value):
    """read array file fields
    """
    if value is None:
        return

    if value.endswith('npy'):
        value = np.load(value)
    elif value.endswith('csv'):
        value = pd.read_csv(value).values
    elif value.endswith('pkl'):
        with open(value, 'rb') as f:
            value = pickle.load(f)

    assert isinstance(value, np.ndarray)
    return value


def recarray_reader(value):
    """read recarray file fields
    """
    if value is None:
        return

    return frame_reader(value).to_records(False)


def frame_reader(value):
    """read pandas dataframes file fields
    """

    if value is None:
        return

    if value.endswith('csv'):
        value = pd.read_csv(value)
    elif value.endswith('pkl'):
        with open(value, 'rb') as f:
            value = pickle.load(f)
    elif value.endswith('npy'):
        value = pd.DataFrame(np.load(value))
    elif value.endswith('json'):
        value = pd.DataFrame(json_reader(value))

    assert isinstance(value, pd.DataFrame)
    return value


def series_reader(value):
    """read pandas series file fields
    """

    return pd.Series(json_reader(value))


class ListReader:

    def __init__(self, func):

        self.func = func

    def __call__(self, value):

        if value is None:
            return

        return [self.func(val) for val in value]


class TupleReader:

    def __init__(self, func):

        self.func = func

    def __call__(self, value):

        if value is None:
            return

        return (
            None
            if val is None
            else self.func(val)
            for val in value
        )


class DictReader:

    def __init__(self, func_dict):
        self.func_dict = func_dict

    def __call__(self, value):

        if value is None:
            return

        for key, func in self.func_dict.items():
            if value[key] is None:
                pass
            else:
                value[key] = func(value[key])

        return value


class EnumReader:

    def __init__(self, value, choices):

        self.value = value
        self.choices = choices

    def __call__(self, value):

        if value is None:
            return

        index = self.choices.index(value)
        return self.value[index]


class DbReader:

    def __init__(self, table_class, columns):

        self.table_class = table_class
        self.columns = columns

    def __call__(self, value):

        if value is None:
            return

        value = literal_eval(value)
        restrict = {
            key: val
            for val, key in zip(value, self.table_class.primary_key)
        }

        entry = self.table_class & restrict
        data = entry.fetch1()

        if isinstance(self.columns, str):
            return data[self.columns]
        else:
            return [data[col] for col in self.columns]
