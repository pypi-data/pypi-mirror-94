import logging
import typing
from PySide2 import QtCore

from famegui import models
from famegui.agent_controller import AgentController
from famegui.appworkingdir import AppWorkingDir


class ScenarioProperties(QtCore.QObject):
    """ Class used to attach extra properties to a scenario model and signal when they change """

    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        logging.debug("initializing scenario properties")
        self.reset()

    def reset(self, schema: models.Schema = None, file_path=""):
        self._has_unsaved_changes = False
        self._file_path = file_path
        self._schema = schema
        self.changed.emit()

    @property
    def has_data(self) -> bool:
        return self._schema is not None

    @property
    def has_unsaved_changes(self) -> bool:
        return self._has_unsaved_changes

    def set_unsaved_changes(self, has_changes: bool):
        assert self.has_data
        if self._has_unsaved_changes != has_changes:
            self._has_unsaved_changes = has_changes
            self.changed.emit()

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def schema(self) -> models.Schema:
        assert self._schema is not None
        return self._schema

    @property
    def schema_name(self) -> str:
        return self.schema.name

    def set_file_path(self, file_path: str):
        assert self.has_data
        if self._file_path != file_path:
            self._file_path = file_path
            self.changed.emit()


class ScenarioController(QtCore.QObject):
    selected_agent_changed = QtCore.Signal(AgentController)
    # added agent
    agent_added = QtCore.Signal(AgentController)
    # sender, receiver, contract
    contract_added = QtCore.Signal(
        AgentController, AgentController, models.Contract)

    def __init__(self, working_dir: AppWorkingDir):
        super().__init__()
        logging.debug("initializing scenario controller")
        self._working_dir = working_dir
        self._scenario_model = None
        self._agents = {}
        self._contracts = {}
        self._properties = ScenarioProperties()

    def reset(self):
        self._agents = {}
        self._contracts = {}
        self._properties.reset()
        self._scenario_model = None

    @property
    def has_data(self) -> bool:
        return self._scenario_model is not None and self.properties.has_data

    @property
    def has_unsaved_changes(self) -> bool:
        return self.properties.has_unsaved_changes

    @property
    def properties(self) -> ScenarioProperties:
        return self._properties

    @property
    def schema(self) -> models.Schema:
        return self._properties.schema

    @property
    def agent_list(self) -> typing.List[AgentController]:
        assert self.has_data
        return self._agents.values()

    def generate_new_agent_id(self):
        new_id = len(self._agents) + 1
        # note: we don't control how ids have been generated for agents created from an external source
        # so we check for possible conflict and solve it
        if new_id in self._agents:
            for i in range(1, len(self._agents) + 2):
                if not i in self._agents:
                    new_id = i
                    break
        logging.debug("generated new agent id {}".format(new_id))
        return new_id

    # the given agent id can be 0 to clear the current selection
    def set_selected_agent_id(self, agent_id: int):
        assert self.has_data
        if agent_id not in self._agents:
            assert agent_id == 0 or agent_id is None
            self.selected_agent_changed.emit(None)
        else:
            self.selected_agent_changed.emit(self._agents[agent_id])

    def add_new_agent(self, agent_model: models.Agent, x: int, y: int):
        assert self.has_data
        agent_model.set_display_xy(x, y)
        # TODO: use _create_valid_agent_controller once the new agent dialog can provide a valid new agent
        self._tmp_create_agent_controller(agent_model)
        self._scenario_model.add_agent(agent_model)
        self._properties.set_unsaved_changes(True)
        logging.info("created new agent {} of type '{}'".format(
            agent_model.id_str, agent_model.type_name))

    def _tmp_create_agent_controller(self, agent_model: models.Agent):
        assert self.has_data
        agent = AgentController(agent_model)
        self._agents[agent.id] = agent
        self.agent_added.emit(agent)

    def _create_valid_agent_controller(self, agent_model: models.Agent):
        assert self.has_data
        agent = AgentController(agent_model)
        agent.apply_schema(self.schema, self._working_dir)
        self._agents[agent.id] = agent
        self.agent_added.emit(agent)

    def add_new_contract(self, contract_model: models.Contract):
        self._scenario_model.add_contract(contract_model)
        self._create_contract_model(contract_model)
        self._properties.set_unsaved_changes(True)
        logging.info("created new contract '{}' between {} and {}".format(
            contract_model.product_name, contract_model.sender_id_str, contract_model.receiver_id_str))

    def _create_contract_model(self, contract: models.Contract):
        assert self.has_data
        # should be enforced when creating / reading the contract
        assert contract.sender_id != contract.receiver_id

        # validate sender / receiver are known
        if contract.sender_id not in self._agents:
            raise ValueError("can't add contract '{}' because sender agent id '{}' is unknown".format(
                contract.name, contract.sender_id))
        if contract.receiver_id not in self._agents:
            raise ValueError("can't add contract '{}' because receiver agent id '{}' is unknown".format(
                contract.name, contract.receiver_id))

        sender_ctrl = self._agents[contract.sender_id]
        receiver_ctrl = self._agents[contract.receiver_id]

        # connect agents
        sender_ctrl.model.add_output(contract.receiver_id)
        receiver_ctrl.model.add_input(contract.sender_id)

        self.contract_added.emit(sender_ctrl, receiver_ctrl, contract)

    def create_new_scenario(self, schema: models.Schema):
        # don't call this function when a scenario already exists to avoid accidental loss of data
        assert not self.has_data

        self._scenario_model = models.Scenario()
        self._scenario_model.set_schema_name(schema.name)
        self._properties.reset(schema)

    def open_scenario(self, scenario: models.Scenario, file_path: str, schema: models.Schema):
        logging.debug("opening new scenario and schema")
        self.reset()

        changed_done = False
        if scenario.schema_name != schema.name:
            scenario.set_schema_name(schema.name)
            changed_done = True

        try:
            self._scenario_model = scenario
            self._properties.reset(schema, file_path)
            self._properties.set_unsaved_changes(changed_done)

            # process and validate the scenario
            for a in self._scenario_model.agents.values():
                self._create_valid_agent_controller(a)
            for c in self._scenario_model.contracts:
                self._create_contract_model(c)
        except:
            logging.warning(
                "failed to open the scenario with the given schema")
            self.reset()
            raise

    def save_to_file(self, file_path):
        assert self.has_data
        logging.info("saving scenario to file {}".format(file_path))
        models.ScenarioLoader.save_to_yaml_file(
            self._scenario_model, file_path)
        # update status
        self._properties.set_unsaved_changes(False)
        self._properties.set_file_path(file_path)
