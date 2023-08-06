import typing

from famegui import models


class SchemaAgentTypeField:
    """ Represents a field of a schema agent type """

    def __init__(self, field_name: str, field_type: models.SchemaAgentTypeFieldType):
        assert field_name != ""
        self._name = field_name
        self._type = field_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> models.SchemaAgentTypeFieldType:
        return self._type
