from utils import AlgorithmException, U
from models import Criticality, Task, TaskType
from typing import List


TASKS: List[Task] = [
    Task(30, Criticality.HI, 3, 4.5),
    Task(100, Criticality.HI, 5, 12),
    Task(200, Criticality.LO, 10),
    Task(50, Criticality.LO, 3),
    Task(50, Criticality.LO, 7),
]


def main():
    global TASKS
    # Append re-executions
    TASKS += [t.get_re_execution() for t in TASKS]

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
                return x
        return x


if __name__ == "__main__":
    try:
        x = main()
        print(f"{x}")
        exit(0)
    except AlgorithmException as ae:
        print(f"Algorithm Error: {ae}")
        exit(127)
