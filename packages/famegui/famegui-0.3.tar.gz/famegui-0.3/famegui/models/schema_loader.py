import logging
import os

from famegui import models
import famegui.models.yaml_utils as yaml_utils


def _extract_field(field_name, items) -> models.SchemaAgentTypeField:
    field_type = yaml_utils.must_get_str_key(items, "FieldType")
    # optional fields
    is_mandatory = items.get("Mandatory")
    enum_values = items.get("Values")

    field_type = models.SchemaAgentTypeFieldType(
        field_type, is_mandatory, enum_values)
    return models.SchemaAgentTypeField(field_name, field_type)


def _extract_input(agent_type_name, items) -> models.SchemaAgentType:
    result = models.SchemaAgentType(agent_type_name)
    inputs = items.get("Inputs")
    if inputs is None:
        logging.warning(
            "no input defined in schema for agent type '{}'".format(agent_type_name))
    else:
        for input_name, input_items in inputs.items():
            logging.debug("loading input '{}.{}'".format(
                agent_type_name, input_name))
            result.add_field(_extract_field(input_name, input_items))
    return result


def _load_schema_file(schema_name: str, file_path: str) -> models.Schema:
    file_path = os.path.abspath(file_path)
    yaml_dict = yaml_utils.must_load_file(file_path)

    if yaml_dict is None or not "AgentTypes" in yaml_dict:
        raise ValueError("at least one agent type must be defined")

    result = models.Schema(schema_name)
    for name, items in yaml_dict.get("AgentTypes").items():
        logging.debug("loading agent type {}".format(name))
        if items is None:
            # we accept agent types with no details
            logging.warning(
                "definition of agent type '{}' is empty".format(name))
        else:
            result.add_agent_type(_extract_input(name, items))

    return result


class SchemaLoader:
    """ Class to load and parse schema files """
    @staticmethod
    def load_yaml_file(schema_name: str, file_path: str) -> models.Schema:
        logging.info("loading schema file {}".format(file_path))
        try:
            return _load_schema_file(schema_name, file_path)
        except Exception as e:
            raise ValueError(
                "failed to load schema file {}".format(file_path)) from e
