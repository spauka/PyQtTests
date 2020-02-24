from typing import List
from Qt import QtCore, QtGui, QtWidgets

class Chip(QtWidgets.QGraphicsItem):
    def __init__(self, color: QtGui.QColor, x: float, y: float):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.setZValue((x + y)%2)
        self.stuff: List[QtCore.QPointF] = []

        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable |
                      QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def boundingRect(self) -> QtCore.QRectF:
        return QtCore.QRectF(0, 0, 110, 70)

    def shape(self) -> QtGui.QPainterPath:
        path = QtGui.QPainterPath()
        path.addRect(14, 14, 82, 42)
        return path

    def paint(self, p: QtGui.QPainter, option: QtWidgets.QGraphicsItem.ItemIsSelectable,
              widget: QtWidgets.QWidget): # pylint: disable=unused-argument

        # Set color when selected
        if option.state & QtWidgets.QStyle.State_Selected:
            fillColor = self.color.darker(150)
        else:
            fillColor = self.color

        # Lighten if mouse over
        if option.state & QtWidgets.QStyle.State_MouseOver:
            fillColor = fillColor.lighter(125)

        # Calculate level of detail
        lod = option.levelOfDetailFromTransform(p.worldTransform())
        if lod < 0.125:
            p.fillRect(QtCore.QRectF(0, 0, 110, 70), fillColor)
            return
        if lod < 0.2:
            oldBrush = p.brush()
            p.setBrush(fillColor)
            p.drawRect(13, 13, 97, 57)
            p.setBrush(oldBrush)
            return

        oldPen = p.pen()
        oldBrush = p.brush()

        # Use a copy of the old pen
        pen = QtGui.QPen(oldPen)
        if option.state & QtWidgets.QStyle.State_Selected:
            pen.setWidth(2)
        else:
            pen.setWidth(0)
        p.setPen(pen)

        # Draw the inside of the chip
        if option.state & QtWidgets.QStyle.State_Sunken:
            p.setBrush(QtGui.QBrush(fillColor.darker(120)))
        else:
            p.setBrush(QtGui.QBrush(fillColor.darker(100)))
        p.drawRect(QtCore.QRect(14, 14, 79, 39))
        p.setBrush(oldBrush)

        if lod >= 1:
            p.setPen(QtGui.QPen(QtCore.Qt.gray, 1))
            p.drawLine(15, 54, 94, 54)
            p.drawLine(94, 53, 94, 15)
            p.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        if lod >= 2:
            font = QtGui.QFont("Times", 10)
            font.setStyleStrategy(QtGui.QFont.ForceOutline)
            p.setFont(font)
            p.save()
            p.scale(0.1, 0.1)
            p.drawText(170, 180, f"Model: VSC-2000 (Very Small Chip) at {self.x}x{self.y}")
            p.drawText(170, 200, "Serial number: DLWR-WEER-123L-ZZ33-SDSJ")
            p.drawText(170, 220, "Manufacturer: Chip Manufacturer")
            p.restore()

        lines = []
        if lod >= 0.5:
            for i in range(0, 11, 1 if lod > 0.5 else 2):
                lines.append(QtCore.QLineF(18 + 7*i, 13, 18 + 7*i, 5))
                lines.append(QtCore.QLineF(18 + 7*i, 54, 18 + 7*i, 62))
            for i in range(0, 7, 1 if lod > 0.5 else 2):
                lines.append(QtCore.QLineF(5, 18 + i*5, 13, 18 + i*5))
                lines.append(QtCore.QLineF(94, 18 + i*5, 102, 18 + i*5))
        if lod >= 0.4:
            lines.append(QtCore.QLineF(25, 35, 35, 35))
            lines.append(QtCore.QLineF(35, 30, 35, 40))
            lines.append(QtCore.QLineF(35, 30, 45, 35))
            lines.append(QtCore.QLineF(35, 40, 45, 35))
            lines.append(QtCore.QLineF(45, 30, 45, 40))
            lines.append(QtCore.QLineF(45, 35, 55, 35))
        p.drawLines(lines)

        # Draw red ink
        if self.stuff:
            p.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine,
                                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            p.setBrush(QtCore.Qt.NoBrush)
            path = QtGui.QPainterPath()
            path.moveTo(self.stuff[0])
            for point in self.stuff[1:]:
                path.lineTo(point)
            p.drawPath(path)

        p.setPen(oldPen)
        p.setBrush(oldBrush)

    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.update()

    def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            self.stuff.append(event.pos())
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.update()
