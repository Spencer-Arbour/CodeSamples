from enum import Enum
from typing import Union

import datetime


class WeightUnit(Enum):
    G = 1
    KG = 1000
    LB = 453.592


class Weight:

    def __init__(self, weight: Union[int, float], weight_unit: WeightUnit):
        self._weight = weight
        self._weight_unit = weight_unit

    @property
    def weight(self):
        return self._weight

    @property
    def weight_unit(self):
        return self._weight_unit

    def _common_weight_convert(self):
        return self._weight * self._weight_unit.value

    def __add__(self, other):
        if type(other) in (int, float):
            return (self._common_weight_convert() + other) / self.weight_unit.value

        elif type(other) is Weight:
            return (self._common_weight_convert() + other._common_weight_convert()) / self._weight_unit.value

        else:
            raise ArithmeticError("Can't implicitly add {0} to weight".format(type(other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        self._weight = self.__add__(other)
        return self

    def __sub__(self, other):
        if type(other) in (int, float):
            return (self._common_weight_convert() - other) / self.weight_unit.value

        elif type(other) is Weight:
            return (self._common_weight_convert() - other._common_weight_convert()) / self._weight_unit.value

        else:
            raise ArithmeticError("Can't implicitly subtract {0} from weight".format(type(other)))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __isub__(self, other):
        self._weight = self.__sub__(other)
        return self

    def __str__(self):
        return "{0:0.2f} {1}".format(self._weight, self._weight_unit.name)
