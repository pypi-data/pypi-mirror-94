import typing
from famegui import models


class Agent:
    """ Represents an agent as defined in a scenario file """

    def __init__(self, id, type_name):
        assert type(id) == int and id >= 0
        assert type(type_name) == str and type_name != ""
        self._id = id
        self._type_name = type_name
        self._inputs = []
        self._outputs = []
        self._attributes = {}
        self._display_x = None
        self._display_y = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def id_str(self) -> str:
        return "#{}".format(self._id)

    @property
    def type_name(self) -> str:
        return self._type_name

    @property
    def inputs(self) -> typing.List[int]:
        return self._inputs

    def add_input(self, agent_id):
        self._inputs.append(agent_id)

    @property
    def outputs(self) -> typing.List[int]:
        return self._outputs

    def add_output(self, agent_id):
        self._outputs.append(agent_id)

    @property
    def attributes(self) -> typing.Dict[str, typing.Any]:
        return self._attributes

    def add_attribute(self, name: str, value: typing.Any):
        if name in self._attributes:
            raise ValueError(
                "can't add attribute '{}' to agent {} because it already exists".format(name, self.id_str))
        self._attributes[name] = value

    @property
    def display_xy(self) -> typing.List[int]:
        if self._display_x is None or self._display_y is None:
            return None
        return [self._display_x, self._display_y]

    def set_display_xy(self, x, y):
        self._display_x = x
        self._display_y = y
