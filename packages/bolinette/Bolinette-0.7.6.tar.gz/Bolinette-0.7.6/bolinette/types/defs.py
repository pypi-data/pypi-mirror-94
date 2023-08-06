from typing import Union, Literal

from bolinette import types


class Reference:
    def __init__(self, model_name: str, column_name: str):
        self.model_name = model_name
        self.column_name = column_name

    def __repr__(self):
        return f'<Reference -> {self.model_name}.{self.column_name}'


class Column:
    def __init__(self, data_type: 'types.db.DataType', *, reference: Reference = None, primary_key: bool = False,
                 nullable: bool = True, unique: bool = False, model_id: bool = False, default=None):
        self.type = data_type
        self.reference = reference
        self.primary_key = primary_key
        self.nullable = nullable
        self.unique = unique
        self.model_id = model_id
        self.name = None
        self.default = default

    def __repr__(self):
        return f'<Column {self.name}: {repr(self.type)}>'


class Backref:
    def __init__(self, key: str, *, lazy: bool = True):
        self.key = key
        self.lazy = lazy

    def __repr__(self):
        return f'<Backref <- {self.key}' + (' lazy ' if self.lazy else '') + '>'


class Relationship:
    def __init__(self, model_name: str, *, backref: Backref = None, foreign_key: Column = None,
                 lazy: Union[bool, Literal['subquery']] = False, secondary: str = None, remote_side: Column = None):
        self.model_name = model_name
        self.foreign_key = foreign_key
        self.backref = backref
        self.secondary = secondary
        self.remote_side = remote_side
        self.lazy = lazy
        self.name = None

    def __repr__(self):
        return f'<Relationship {self.name} -> {self.model_name}' + (' lazy ' if self.lazy else '') + '>'
