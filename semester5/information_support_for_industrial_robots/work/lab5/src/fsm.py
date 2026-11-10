"""Finite-state model of the two-robot sorting cell.

The model is deliberately independent from CoppeliaSim.  It documents the
legal transitions and makes the controller testable without the simulator.
"""

from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    SPAWN = auto()
    FEED = auto()
    P1_APPROACH = auto()
    P1_GRASP = auto()
    P1_TRANSFER = auto()
    P1_RELEASE = auto()
    P1_RETURN = auto()
    VISION = auto()
    P2_APPROACH = auto()
    P2_GRASP = auto()
    P2_TRANSFER = auto()
    P2_RELEASE = auto()
    RETURN = auto()
    FAULT = auto()


# FAULT has the highest priority in the controller: it is permitted from every
# normal state when a command timeout or a sensor error occurs.
NEXT = {
    State.IDLE: {State.SPAWN},
    State.SPAWN: {State.FEED},
    State.FEED: {State.P1_APPROACH},
    State.P1_APPROACH: {State.P1_GRASP},
    State.P1_GRASP: {State.P1_TRANSFER},
    State.P1_TRANSFER: {State.P1_RELEASE},
    State.P1_RELEASE: {State.P1_RETURN},
    State.P1_RETURN: {State.VISION},
    State.VISION: {State.P2_APPROACH},
    State.P2_APPROACH: {State.P2_GRASP},
    State.P2_GRASP: {State.P2_TRANSFER},
    State.P2_TRANSFER: {State.P2_RELEASE},
    State.P2_RELEASE: {State.RETURN},
    State.RETURN: {State.SPAWN, State.IDLE},
    State.FAULT: {State.IDLE},
}


def can_transition(current: State, following: State) -> bool:
    """Return True for a normal transition or an emergency transition."""
    return following is State.FAULT or following in NEXT[current]
