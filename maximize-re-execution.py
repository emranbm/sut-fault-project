from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class Criticality(Enum):
    LO = 1
    HI = 2


@dataclass
class Task:
    P: float
    X: Criticality
    CLO: float
    CHI: Optional[float] = None

    def C(self, criticality: Criticality):
        if criticality == Criticality.LO:
            return self.CLO
        else:
            return self.CHI


TASKS: List[Task] = [
    Task(30, Criticality.HI, 3, 4.5),
    Task(100, Criticality.HI, 5, 12),
    Task(200, Criticality.LO, 10),
    Task(50, Criticality.LO, 3),
    Task(50, Criticality.LO, 7),
]


def U(tasks: List[Task], system_criticality: Criticality, task_criticality: Criticality):
    if system_criticality == Criticality.LO and task_criticality == Criticality.HI:
        raise Exception(
            "Invalid State! Task Criticality higher than System Criticality.")
    included_tasks = [t for t in tasks if t.X == system_criticality]
    return sum([t.C(task_criticality) / t.P for t in included_tasks])


def main():
    print(U(TASKS, Criticality.HI, Criticality.LO))


if __name__ == "__main__":
    exit(main())
