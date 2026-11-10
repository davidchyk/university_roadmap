"""Offline tests for normal, fault and recovery transitions."""

from pathlib import Path

from fsm import State, can_transition
from main import SortingController


def test_normal_cycle():
    sequence = [
        State.IDLE, State.SPAWN, State.FEED, State.P1_APPROACH, State.P1_GRASP,
        State.P1_TRANSFER, State.P1_RELEASE, State.P1_RETURN, State.VISION,
        State.P2_APPROACH, State.P2_GRASP, State.P2_TRANSFER, State.P2_RELEASE,
        State.RETURN, State.SPAWN,
    ]
    assert all(can_transition(a, b) for a, b in zip(sequence, sequence[1:]))


def test_timeout_has_priority():
    assert can_transition(State.P1_TRANSFER, State.FAULT)
    assert can_transition(State.VISION, State.FAULT)


def test_reset_recovers_from_fault():
    assert can_transition(State.FAULT, State.IDLE)


def test_colour_response_formats():
    assert SortingController.extract_rgb([1.0, 0.05, 0.05]) == [1.0, 0.05, 0.05]
    assert SortingController.extract_rgb([[0.05, 0.90, 0.08]]) == [0.05, 0.90, 0.08]
    assert SortingController.extract_rgb([]) is None


def simulate_fault_recovery() -> list[str]:
    """Model the sensor-error input and operator recovery without CoppeliaSim."""
    trace = [
        (State.IDLE, State.SPAWN, "START command"),
        (State.SPAWN, State.FEED, "ball created"),
        (State.FEED, State.P1_APPROACH, "ball in pickup zone"),
        (State.P1_APPROACH, State.P1_GRASP, "Picker1 position confirmed"),
        (State.P1_GRASP, State.P1_TRANSFER, "grasp confirmed"),
        (State.P1_TRANSFER, State.P1_RELEASE, "table position confirmed"),
        (State.P1_RELEASE, State.P1_RETURN, "ball released"),
        (State.P1_RETURN, State.VISION, "Picker1 home"),
        (State.VISION, State.FAULT, "camera returned no colour"),
        (State.FAULT, State.IDLE, "RESET command"),
        (State.IDLE, State.SPAWN, "repeated START command"),
    ]
    lines = ["step | transition | cause"]
    for step, (source, target, cause) in enumerate(trace):
        assert can_transition(source, target)
        lines.append(f"{step:>4} | {source.name} -> {target.name} | {cause}")
    return lines


if __name__ == "__main__":
    test_normal_cycle()
    test_timeout_has_priority()
    test_reset_recovers_from_fault()
    test_colour_response_formats()
    trace = simulate_fault_recovery()
    log_path = Path(__file__).resolve().parents[1] / "logs" / "fault_recovery_test.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(trace) + "\n", encoding="utf-8")
    print("FSM transition tests: OK")
