from enum import Enum
from dataclasses import dataclass
from typing import Optional

class Criticality(Enum):
    LO = 1
    HI = 2


class TaskType(Enum):
    PRIMARY = 1
    RE_EXECUTION = 2


@dataclass
class Task:
    P: float
    X: Criticality
    CLO: float
    CHI: Optional[float] = None
    TYPE: TaskType = TaskType.PRIMARY

    def C(self, criticality: Criticality):
        if criticality == Criticality.LO:
            return self.CLO
        else:
            return self.CHI or self.CLO

    def u(self, criticality):
        return self.C(criticality) / self.P

    def get_re_execution(self):
        return Task(self.P, self.X, self.CLO, self.CHI, TaskType.RE_EXECUTION)

    def __repr__(self) -> str:
        return f'P={self.P}'