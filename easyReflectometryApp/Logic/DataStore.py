__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'

from abc import abstractmethod
from typing import Union, overload, TypeVar

from easyCore import np
from easyCore.Utils.json import MSONable, MontyDecoder
from collections.abc import Sequence

T = TypeVar('T')


class ProjectData(MSONable):
    def __init__(self, name='DataStore', exp_data=None, sim_data=None):
        self.name = name
        if exp_data is None:
            exp_data = DataStore(name='Exp Datastore')
        if sim_data is None:
            sim_data = DataStore(name='Sim Datastore')
        self.exp_data = exp_data
        self.sim_data = sim_data


class DataStore(Sequence, MSONable):

    def __init__(self, *args, name='DataStore'):
        self.name = name
        self.items = list(args)
        self.show_legend = False

    def __getitem__(self, i: int) -> T:
        return self.items.__getitem__(i)

    def __len__(self) -> int:
        return len(self.items)

    def __setitem__(self, key, value):
        self.items[key] = value

    def append(self, *args):
        self.items.append(*args)

    def as_dict(self, skip: list = []) -> dict:
        this_dict = super(DataStore, self).as_dict(self)
        this_dict['items'] = [
            item.as_dict() for item in self.items if hasattr(item, 'as_dict')
        ]

    @classmethod
    def from_dict(cls, d):
        items = d['items']
        del d['items']
        obj = cls.from_dict(d)
        decoder = MontyDecoder()
        obj.items = [decoder.process_decoded(item) for item in items]
        return obj

    @property
    def experiments(self):
        return [self[idx] for idx in range(len(self)) if self[idx].is_experiment]

    @property
    def simulations(self):
        return [self[idx] for idx in range(len(self)) if self[idx].is_simulation]


class DataSet1D(MSONable):

    def __init__(self, name: str = 'Series',
                 x: Union[np.ndarray, list] = None,
                 y: Union[np.ndarray, list] = None,
                 e: Union[np.ndarray, list] = None,
                 data_type: str = 'simulation',
                 x_label: str = 'x',
                 y_label: str = 'y'):

        if not isinstance(data_type, str):
            raise AttributeError
        self._datatype = None
        self.data_type = data_type

        if x is None:
            x = np.array([])
        if y is None:
            y = np.array([])
        if e is None:
            e = np.zeros_like(x)

        self.name = name
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        if not isinstance(y, np.ndarray):
            y = np.array(y)

        self.x = x
        self.y = y
        self.e = e

        self.x_label = x_label
        self.y_label = y_label

        self._color = None

    @property
    def data_type(self) -> str:
        if self._datatype == 'e':
            r = 'experiment'
        else:
            r = 'simulation'
        return r

    @data_type.setter
    def data_type(self, data_type: str):
        data_switch = data_type.lower()[0]
        if data_switch == 's':
            self._datatype = 's'
        elif data_switch == 'e':
            self._datatype = 'e'

    @property
    def is_experiment(self) -> bool:
        return self._datatype == 'e'

    @property
    def is_simulation(self) -> bool:
        return self._datatype == 's'

    def __repr__(self) -> str:
        return "1D DataStore of '{:s}' Vs '{:s}' with {} data points".format(self.x_label, self.y_label, len(self.x))
