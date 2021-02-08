from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


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


class AlgorithmException(Exception):
    pass


TASKS: List[Task] = [
    Task(30, Criticality.HI, 3, 4.5),
    Task(100, Criticality.HI, 5, 12),
    Task(200, Criticality.LO, 10),
    Task(50, Criticality.LO, 3),
    Task(50, Criticality.LO, 7),
]


def U(tasks: List[Task], system_criticality: Criticality, task_criticality: Criticality, tasks_type: Optional[TaskType] = None):
    if system_criticality == Criticality.LO and task_criticality == Criticality.HI:
        raise AlgorithmException(
            "Invalid State! Task Criticality higher than System Criticality.")
    included_tasks = [t for t in tasks if t.X == system_criticality]
    if tasks_type is not None:
        included_tasks = [t for t in included_tasks if t.TYPE == tasks_type]
    return sum([t.u(task_criticality) for t in included_tasks])

def main():
    global TASKS
    # Append re-executions
    # TASKS += [t.get_re_execution() for t in TASKS]

    # Initialization
    gama = [t for t in TASKS if t.X == Criticality.HI]
    cee = [t for t in TASKS if t.X == Criticality.LO]
    U_HI_LO = U(TASKS, Criticality.HI, Criticality.LO)
    U_HI_HI = U(TASKS, Criticality.HI, Criticality.HI)
    U_LO_LO = U(TASKS, Criticality.LO, Criticality.LO)

    cee = sorted([t for t in cee if t.TYPE == TaskType.PRIMARY],
                 key=lambda t: t.u(Criticality.LO)) \
        + sorted([t for t in cee if t.TYPE == TaskType.RE_EXECUTION],
                 key=lambda t: t.u(Criticality.LO))
    x1 = U_HI_LO / (1 - U_LO_LO)
    x2 = (1 - U_HI_HI) / U_LO_LO
    x = x2

    if x2 < x1:
        raise AlgorithmException(f"Not Schedulable: x2({x2}) < x1({x1})")
    else:
        while len(cee) > 1:
            u_LO = cee[0].u(Criticality.LO)
            U_HI_LO += u_LO
            U_HI_HI += u_LO
            U_LO_LO -= u_LO
            x1 = U_HI_LO / (1 - U_LO_LO)
            x2 = (1 - U_HI_HI) / U_LO_LO
            if x1 <= x2:
                gama.append(cee[0])
                x = x2
                cee.pop(0)
            else:
                return 1 / x
        return 1 / x



if __name__ == "__main__":
    try:
        x = main()
        print(f"{x}")
        exit(0)
    except AlgorithmException as ae:
        print(f"Algorithm Error: {ae}")
        exit(127)
