import typing

from famegui import models


class Schema:
    """ Represents a schema to be applied on a scenario """

    def __init__(self, name: str):
        assert name != ""
        self._name = name
        self._agent_types = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def agent_types(self) -> typing.Dict[str, models.SchemaAgentType]:
        return self._agent_types

    def add_agent_type(self, agent_type: models.SchemaAgentType):
        self._agent_types[agent_type.name] = agent_type

    def agent_type_from_name(self, name: str) -> models.SchemaAgentType:
        return self._agent_types[name] if name in self._agent_types else None
