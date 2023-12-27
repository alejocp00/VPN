import enum


class VPNStatus(enum.Enum):
    """VPNStatus enum."""

    IDLE = 0
    RUNNING = 1
    SHUTING_DOWN = 2


class ProcessStatus(enum.Enum):
    """ProcessStatus enum."""

    IDLE = 0
    RUNNING = 1
    ERROR = 2
    DONE = 3


class VPNProtocol(enum.Enum):
    """VPNProtocol enum."""

    UNKNOWN = 0
    UDP = 1
    TCP = 2
