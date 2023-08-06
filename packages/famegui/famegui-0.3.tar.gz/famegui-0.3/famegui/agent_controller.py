import logging
import typing
import os

from famegui import models, colorpalette
from famegui.appworkingdir import AppWorkingDir


class AgentController(models.Agent):
    """ Controller attached to a FAME Agent to sync it with the views """

    def __init__(self, agent: models.Agent):
        self.model = agent
        self.tree_item = None
        self.scene_item = None

    @property
    def id(self) -> int:
        return self.model.id

    @property
    def id_str(self) -> str:
        return self.model.id_str

    @property
    def type_name(self) -> str:
        return self.model.type_name

    @property
    def attributes(self) -> typing.Dict[str, str]:
        return self.model.attributes

    @property
    def tooltip_text(self) -> str:
        text = "<font size='4'><b>{}</b></font>".format(self.model.type_name)

        text += "<table border=0 cellpadding=2 style='border-collapse: collapse'><tbody>"
        text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
            "ID", self.model.id_str)
        for k, v in self.model.attributes.items():
            text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(k, v)

        text += "</tbody></table>"
        return text

    @property
    def svg_color(self) -> str:
        return colorpalette.color_for_agent_type(self.type_name)

    @property
    def x(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[0]

    @property
    def y(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[1]

    def apply_schema(self, schema: models.Schema, working_dir: AppWorkingDir):
        logging.debug("validating agent {} of type '{}' with schema '{}'".format(
            self.id_str, self.type_name, schema.name))
        agent_type = schema.agent_type_from_name(self.type_name)
        if agent_type is None:
            raise ValueError("invalid agent {}: agent type '{}' is not defined by schema '{}'".format(
                self.id_str, self.type_name, schema.name))

        # validate the existing attributes
        for attr_name, attr_value in self.attributes.items():
            attr_full_name = "{}.{}".format(self.type_name, attr_name)
            if not attr_name in agent_type.fields:
                raise ValueError("invalid agent {}: attribute '{}' is not defined by schema '{}'".format(
                    self.id_str, attr_full_name, schema.name))
            else:
                field_type = agent_type.fields[attr_name].type
                if not field_type.is_compatible_value(attr_value):
                    raise ValueError("invalid agent {}: value '{}' of attribute '{}' is rejected by schema '{}'".format(
                        self.id_str, attr_value, attr_full_name, schema.name))
                if field_type.type == models.FieldType.TIME_SERIES:
                    # validate timeseries file path
                    file_path = working_dir.find_existing_child_file(
                        attr_value)
                    if not os.path.isfile(file_path):
                        raise ValueError("invalid agent {}: time series file '{}' not found in FAME working directory '{}'".format(
                            self.id_str, attr_value, working_dir))

        # find missing attributes
        for f in agent_type.fields.values():
            if f.name not in self.attributes:
                if f.type.is_mandatory:
                    raise ValueError("invalid agent {}: mandatory attribute '{}' is not defined".format(
                        self.id_str, f.name))
                else:
                    logging.info("agent {} does not define optional attribute '{}'".format(
                        self.id_str, f.name))
