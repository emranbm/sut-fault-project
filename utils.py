from models import Criticality, Task, TaskType
from typing import List, Optional

class AlgorithmException(Exception):
    pass

def U(tasks: List[Task], system_criticality: Criticality, task_criticality: Criticality, tasks_type: Optional[TaskType] = None):
    if system_criticality == Criticality.LO and task_criticality == Criticality.HI:
        raise AlgorithmException(
            "Invalid State! Task Criticality higher than System Criticality.")
    included_tasks = [t for t in tasks if t.X == system_criticality]
    if tasks_type is not None:
        included_tasks = [t for t in included_tasks if t.TYPE == tasks_type]
    return sum([t.u(task_criticality) for t in included_tasks])