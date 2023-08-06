from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QGraphicsItem

import weakref
import math
import logging


class ContractGraphItem(QtWidgets.QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, sourceNode, destNode):
        QGraphicsItem.__init__(self)
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)

        self._arrow_size = 10.0
        self._draw_line = QtCore.QLineF()
        self.source = weakref.ref(sourceNode)
        self.dest = weakref.ref(destNode)
        self.source().addEdge(self)
        self.dest().addEdge(self)
        self.adjust()

    def type(self):
        """ override QGraphicsItem.type() """
        return ContractGraphItem.Type

    def sourceNode(self):
        return self.source()

    def setSourceNode(self, node):
        self.source = weakref.ref(node)
        self.adjust()

    def destNode(self):
        return self.dest()

    def setDestNode(self, node):
        self.dest = weakref.ref(node)
        self.adjust()

    def adjust(self):
        # reset drawing
        self._draw_line = QtCore.QLineF()

        if not self.source() or not self.dest():
            return

        radius = 50
        src_center = self.mapFromItem(self.source(), radius, radius)
        dest_center = self.mapFromItem(self.dest(), radius, radius)

        # compute the distance between the two items
        [src_x, src_y] = src_center.toTuple()
        [dest_x, dest_y] = dest_center.toTuple()
        distance = math.sqrt((src_x - dest_x)**2 + (src_y - dest_y)**2)
        if distance <= radius * 2:
            logging.info("items are too close to draw a line")
            return

        distance_x = dest_x - src_x
        distance_y = dest_y - src_y

        offset_ratio = radius * 1.0 / distance
        offset_x = distance_x * offset_ratio
        offset_y = distance_y * offset_ratio

        centerOffset = QtCore.QPointF(offset_x, offset_y)

        self.prepareGeometryChange()
        line_start = src_center + centerOffset
        line_end = dest_center - centerOffset
        self._draw_line = QtCore.QLineF(line_start, line_end)

    def boundingRect(self):
        if not self.source() or not self.dest():
            return QtCore.QRectF()

        penWidth = 1
        extra = (penWidth + self._arrow_size) / 2.0

        size = QtCore.QSizeF(self._draw_line.x2() - self._draw_line.x1(),
                             self._draw_line.y2() - self._draw_line.y1())
        return QtCore.QRectF(self._draw_line.p1(), size).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source() or not self.dest():
            return

        # Draw the line itself.
        if self._draw_line.length() == 0.0:

            return

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(self._draw_line)

        # Draw the arrows if there's enough room.
        angle = math.acos(self._draw_line.dx() / self._draw_line.length())
        if self._draw_line.dy() >= 0:
            angle = (2.0 * math.pi) - angle

        line_end = self._draw_line.p2()
        destArrowP1 = line_end + QtCore.QPointF(math.sin(angle - math.pi / 3) * self._arrow_size,
                                                math.cos(angle - math.pi / 3) * self._arrow_size)
        destArrowP2 = line_end + QtCore.QPointF(math.sin(angle - math.pi + math.pi / 3) * self._arrow_size,
                                                math.cos(angle - math.pi + math.pi / 3) * self._arrow_size)

        painter.setBrush(QtCore.Qt.black)
        painter.drawPolygon(QtGui.QPolygonF(
            [self._draw_line.p2(), destArrowP1, destArrowP2]))


class AgentGraphItem(QtWidgets.QGraphicsItem):
    Type = QGraphicsItem.UserType + 2

    def __init__(self, agent_id, label, color):
        QGraphicsItem.__init__(self)
        # public
        self.edgeList = []
        # private / read only
        self._label = "#{}".format(agent_id)
        self._color = color
        self._radius = 50
        self._agent_id = agent_id
        self._links = []
        # customize graphics item
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def type(self):
        """ override QGraphicsItem.type() """
        return AgentGraphItem.Type

    def addEdge(self, edge):
        self.edgeList.append(weakref.ref(edge))
        edge.adjust()

    @property
    def agent_id(self) -> int:
        return self._agent_id

    def add_link(self, link):
        self._links.append(link)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self._radius * 2, self._radius * 2)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge().adjust()
            # print("moved {} {}".format(self.x(), self.y()))
            #pass
        return QGraphicsItem.itemChange(self, change, value)

    def paint(self, painter, option, widget=None):
        """ Qt paint method """

        # main rectangle with its border
        if option.state & QtWidgets.QStyle.State_Selected:
            background_color = QtGui.QColor(self._color).darker()
            border_color = QtGui.QColor("#ff009a")
            border_width = 3
        else:
            background_color = QtGui.QColor(self._color)
            border_color = QtGui.QColor(0, 0, 0)
            border_width = 2

        item_rect = self.boundingRect()

        painter.setBrush(QtGui.QBrush(background_color))
        painter.setPen(QtGui.QPen(border_color, border_width))
        painter.drawEllipse(item_rect)

        # label
        font = QtGui.QFont("Arial", 14)
        font.setStyleStrategy(QtGui.QFont.ForceOutline)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 1))
        painter.drawText(item_rect, QtCore.Qt.AlignCenter, self._label)
