from abc import abstractmethod

from magpie.core import AbstractModel


class AbstractLineModel(AbstractModel):
    @abstractmethod
    def do_replace(cls, software, op, new_contents, modification_points):
        pass

    @abstractmethod
    def do_insert(cls, software, op, new_contents, modification_points):
        pass

    @abstractmethod
    def do_delete(cls, software, op, new_contents, modification_points):
        pass
