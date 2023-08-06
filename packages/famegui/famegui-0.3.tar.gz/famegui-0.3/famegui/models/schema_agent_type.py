import typing
from famegui import models


class SchemaAgentType:
    """ Represents a schema agent type """

    def __init__(self, name: str):
        assert name != ""
        self._name = name
        self._fields = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def fields(self) -> typing.Dict[str, models.SchemaAgentTypeField]:
        return self._fields

    def add_field(self, field: models.SchemaAgentTypeField):
        if field.name in self._fields:
            raise ValueError("can't add field '{}' to agent type '{}' because it already exists".format(
                field.name, self.name))
        self._fields[field.name] = field
