from PySide2 import QtCore, QtGui, QtWidgets

from famegui.scenario_graph_view_items import AgentGraphItem, ContractGraphItem
from famegui.agent_controller import AgentController


class ScenarioGraphView(QtWidgets.QGraphicsScene):
    """ View responsible of displaying the scenario as a graph """

    # (x, y)
    agent_creation_requested = QtCore.Signal(int, int)
    # (sender_id, receiver_id)
    contract_creation_requested = QtCore.Signal(int, int)
    # agent_id (can be None)
    selected_agent_changed = QtCore.Signal(int)

    def __init__(self, parent=None):
        QtWidgets.QGraphicsScene.__init__(self, parent)
        self.selectionChanged.connect(self._on_scene_selection_changed)

    @property
    def selected_agent_id(self):
        items = self.selectedItems()
        if len(items) == 1:
            item = items[0]
            assert(item.type() == AgentGraphItem.Type)
            return item.agent_id
        return None

    def add_agent(self, agent: AgentController):
        assert agent.scene_item is None
        # create item
        item = AgentGraphItem(
            agent.id, agent.type_name, agent.svg_color)
        item.setToolTip(agent.tooltip_text)
        item.setPos(agent.x, agent.y)
        # add item
        self.addItem(item)
        agent.scene_item = item

    def add_contract(self, sender: AgentController, receiver: AgentController):
        self.addItem(ContractGraphItem(sender.scene_item, receiver.scene_item))

    def mouseDoubleClickEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        click_pos = event.scenePos()
        # is the double click on an agent item?
        for item in self.items(click_pos):
            if item.type() == AgentGraphItem.Type:
                return

        self.agent_creation_requested.emit(click_pos.x(), click_pos.y())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            click_pos = event.scenePos()
            for item in self.items(click_pos):
                if item.type() == AgentGraphItem.Type:
                    self._on_agent_right_clicked(item.agent_id)
                    return
        QtWidgets.QGraphicsScene.mousePressEvent(self, event)

    def _on_agent_right_clicked(self, agent_id):
        source_id = self.selected_agent_id
        if source_id is not None and source_id != agent_id:
            self.contract_creation_requested.emit(source_id, agent_id)

    def _on_scene_selection_changed(self):
        self.selected_agent_changed.emit(self.selected_agent_id)
