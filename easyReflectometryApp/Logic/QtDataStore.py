__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from typing import List
from PySide2.QtCore import QPointF


class QtDataStore():
    def __init__(self, x, y, sy, y_opt):
        self.x = x
        self.y = y
        self.sy = sy
        self.y_opt = y_opt

    def get_XY(self) -> List[QPointF]:
        return [QPointF(x, y) for x, y in zip(self.x, self.y)]

    def get_lowerXY(self) -> List[QPointF]:
        return [QPointF(x, y - sy) for x, y, sy in zip(self.x, self.y, self.sy)]

    def get_upperXY(self) -> List[QPointF]:
        return [QPointF(x, y + sy) for x, y, sy in zip(self.x, self.y, self.sy)]

    def get_fit_XY(self):
        return [QPointF(x, y) for x, y in zip(self.x, self.y_opt)]
