"""Base classes for tables
"""

COMMENTS = 'comments = null : varchar(4000)'
DESCRIPTION = 'description = null : varchar(4000) # (detailed) description'
PRIMARY_NAME = '{name} : <lookupname> # {comment}'
TAGS = 'tags = null : <tags> # comma-separated tags'
DICTTAGS = 'dict = null: <dicttags> # comma-separated tags with key=value format'
NEURAL_RECORDING = f"""
    recording_id : int auto_increment # integer id number
    ---
    recording_file_id : varchar(63) # recording file identifier -- e.g. prairieview extension
    -> subjects.FlySubject
    -> recordings.RecordingType
    -> recordings.RecordingSolution
    recording_temperature = null : float # recording temperature in Celsius
    recording_time = CURRENT_TIMESTAMP : timestamp # time of recording
    completed = 0 : <truebool> # was the recording completed as intended
    {TAGS}
    {DICTTAGS}
    {COMMENTS}
    """


class FilesMixin:
    """Part table mixin for given a master table multiple files.
    """

    @property
    def definition(self):
        return """
        -> master
        -> core.FileLookupName
        ---
        a_file : attach@attachstore
        """


class DataMixin:
    """Part table mixin for given a master table multiple files.
    """

    @property
    def definition(self):
        return """
        -> master
        -> core.DataLookupName
        ---
        a_datum : blob@datastore
        """


class ExtensionMixin:
    """Part table mixin for given a master table multiple extensions
    (not actual files).
    """

    @property
    def definition(self):
        return """
        -> master
        -> core.ExtensionLookupName
        ---
        an_extension : varchar(63)
        -> [nullable] core.LookupRegex
        """


class ManualLookup:
    """Manual table mixin with given definition
    """

    primary_comment = "short name identifier"

    @property
    def definition(self):
        return f"""
        {PRIMARY_NAME.format(name=self.table_name, comment=self.primary_comment)}
        ---
        {COMMENTS}
        """
