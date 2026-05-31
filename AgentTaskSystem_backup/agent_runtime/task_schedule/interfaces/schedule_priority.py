from enum import IntEnum


class SchedulePriority(IntEnum):
    LOW = 1
    NORMAL = 5
    HIGH = 10
    CRITICAL = 20
