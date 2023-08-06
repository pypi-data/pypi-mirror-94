import logging
import os

from famegui.models import Scenario, Agent, Contract, layout_agents
import famegui.models.yaml_utils as yaml_utils


def _extract_contract(contract_number, contract_dict):
    logging.debug("loading contract number {}".format(contract_number))
    try:
        sender_id = yaml_utils.must_get_int_key(contract_dict, "SenderId")
        receiver_id = yaml_utils.must_get_str_key(contract_dict, "ReceiverId")
        product_name = yaml_utils.must_get_str_key(
            contract_dict, "ProductName")
        return Contract(sender_id, receiver_id, product_name)
    except Exception as e:
        raise ValueError(
            "failed to load contract number '{}'".format(contract_number)) from e


def _extract_agent(agent_number, agent_dict):
    logging.debug("loading agent number {}".format(agent_number))
    try:
        agent_id = yaml_utils.must_get_int_key(agent_dict, "Id")
        if agent_id < 0:
            raise ValueError(
                "invalid id '{}' (must be a positive integer)".format(agent_id))
        agent_type = yaml_utils.must_get_str_key(agent_dict, "Type")
        agent = Agent(agent_id, agent_type)

        # load attributes
        fields_dict = agent_dict.get("Attributes")
        if fields_dict is not None:
            for name, value in fields_dict.items():
                agent.add_attribute(name, value)

        return agent
    except Exception as e:
        raise ValueError(
            "failed to load agent number {}".format(agent_number)) from e


def _check_all_agents_have_display_coords(agents):
    if len(agents) == 0:
        return True
    for _, a in agents.items():
        if a.display_xy is None:
            return False
        return True


def _agent_to_dict(agent: Agent):
    result = {}
    result["Type"] = agent.type_name
    result["Id"] = agent.id
    result["Attributes"] = agent.attributes
    result["Ext"] = {
        "GUI": {
            "DisplayXY": agent.display_xy,
        }
    }
    return result


def _contract_to_dict(contract: Contract):
    result = {}
    result["SenderId"] = contract.sender_id
    result["ReceiverId"] = contract.receiver_id
    result["ProductName"] = contract.product_name
    return result


def _get_node_children(dict, node_name):
    """ always return a valid dict (possibly empty) containing the children of the given node """
    if dict is None or node_name not in dict:
        return {}
    node = dict.get(node_name)
    if node is None:
        return {}
    return node


class ScenarioLoader:
    @staticmethod
    def load_yaml_file(file_path: str) -> Scenario:
        """ Load (read and parse) a YAML scenario file """
        file_path = os.path.abspath(file_path)
        yaml_dict = yaml_utils.must_load_file(file_path)

        scenario = Scenario()

        # read schema name
        if "Schema" in yaml_dict:
            scenario.set_schema_name(yaml_dict["Schema"])
            logging.info("found schema name {}".format(scenario.schema_name))
        else:
            logging.warning("no schema defined")

        # load agents
        current_agent_number = 1
        for node in _get_node_children(yaml_dict, "Agents"):
            agent = _extract_agent(current_agent_number, node)
            scenario.add_agent(agent)
            current_agent_number += 1
        logging.info("loaded {} agent(s)".format(len(scenario.agents)))

        # load contracts
        current_contract_number = 1
        for node in _get_node_children(yaml_dict, "Contracts"):
            scenario.add_contract(
                _extract_contract(current_contract_number, node))
            current_contract_number += 1
        logging.info("loaded {} contract(s)".format(len(scenario.contracts)))

        # check if layout generation is necessary
        if not _check_all_agents_have_display_coords(scenario.agents):
            layout_agents(scenario)
        assert _check_all_agents_have_display_coords(scenario.agents)

        return scenario

    @staticmethod
    def save_to_yaml_file(scenario: Scenario, file_path: str):
        """ Save the given scenario to a YAML file """
        output = {}

        output["Schema"] = scenario.schema_name

        output["Agents"] = []
        for a in scenario.agents.values():
            output["Agents"].append(_agent_to_dict(a))

        output["Contracts"] = []
        for c in scenario.contracts:
            output["Contracts"].append(_contract_to_dict(c))

        yaml_utils.save_to_file(output, file_path)
