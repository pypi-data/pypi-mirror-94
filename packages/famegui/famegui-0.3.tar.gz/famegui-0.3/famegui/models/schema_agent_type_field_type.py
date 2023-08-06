import typing
from enum import Enum

# copied from fameio FieldValidator.py


class FieldType(Enum):
    INTEGER = 0
    DOUBLE = 1
    ENUM = 2
    TIME_SERIES = 3
    DOUBLE_LIST = 4


def is_compatible(data_type, field_value) -> bool:
    """ Returns true if field type of given `field_value` is compatible to required `field_type`. """
    if data_type is FieldType.INTEGER:
        return isinstance(field_value, int)
    elif data_type is FieldType.DOUBLE:
        return isinstance(field_value, (int, float))
    elif data_type is FieldType.DOUBLE_LIST:
        return all(isinstance(x, (int, float)) for x in field_value)
    elif data_type is FieldType.ENUM:
        return isinstance(field_value, str)
    elif data_type is FieldType.TIME_SERIES:
        return isinstance(field_value, str) and field_value != ""
    return False


def _find_type_by_name(name: str):
    name = name.upper()
    if name in FieldType.__members__:
        return FieldType.__members__[name]
    return None


class SchemaAgentTypeFieldType:
    """ Details about a field type for a schema agent type """

    def __init__(self, type_name: str, is_mandatory: bool, enum_values: typing.List[str] = None):
        field_type = _find_type_by_name(type_name)
        if field_type is None:
            raise ValueError("invalid field type '{}'".format(type_name))

        if field_type == FieldType.ENUM:
            if enum_values is None or len(enum_values) == 0:
                raise ValueError(
                    "values are missing for field type '{}'".format(type_name))
            else:
                for v in enum_values:
                    assert v != ""
        elif enum_values is not None:
            raise ValueError(
                "enum values can't be specified for field type '{}'".format(type_name))

        self._type = field_type
        self._is_mandatory = is_mandatory
        self._enum_values = enum_values

    @property
    def type(self) -> FieldType:
        return self._type

    @property
    def type_name(self) -> str:
        return self._type.name.lower()

    @property
    def is_mandatory(self) -> bool:
        return self._is_mandatory

    @property
    def enum_values(self) -> typing.List[str]:
        return self._enum_values

    def is_compatible_value(self, value) -> bool:
        if is_compatible(self.type, value):
            if self.type == FieldType.ENUM:
                return value in self.enum_values
            return True
        return False
