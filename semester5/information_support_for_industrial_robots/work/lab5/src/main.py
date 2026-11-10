"""External FSM controller for Computer Workshop 5.

The scene is a derivative of CW3: a conveyor feeds coloured balls to Picker1,
Picker1 places a ball on the table, and Picker2 sorts it into a colour bin.
Run build_scene.py once, open main.ttt in CoppeliaSim, then run this file.
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, "/opt/coppeliasim/programming/zmqRemoteApi/clients/python/src")
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

from fsm import State, can_transition


PORT = 23000
SAFE_Z = 0.30
GRASP_Z = 0.13
BALL_Z = 0.105
PICKUP = (-0.49, 0.82)
TABLE = (0.00, 0.55)
COLOURS = {
    "red": [1.0, 0.05, 0.05],
    "green": [0.05, 0.90, 0.08],
    "blue": [0.05, 0.15, 1.0],
}
BINS = {
    "red": (0.22, 0.22, 0.22),
    "green": (0.45, 0.22, 0.22),
    "blue": (0.68, 0.22, 0.22),
}
TIMEOUT = {
    State.FEED: 3.0,
    State.P1_APPROACH: 4.0,
    State.P1_GRASP: 3.0,
    State.P1_TRANSFER: 4.0,
    State.P1_RELEASE: 3.0,
    State.P1_RETURN: 4.0,
    State.VISION: 2.0,
    State.P2_APPROACH: 4.0,
    State.P2_GRASP: 3.0,
    State.P2_TRANSFER: 4.0,
    State.P2_RELEASE: 3.0,
    State.RETURN: 4.0,
}


@dataclass
class Motion:
    target: int
    destination: list[float]


class SortingController:
    """Cyclic Moore-style FSM with timeouts and an explicit recovery path."""

    def __init__(self, sim, log_path: Path, inject_vision_fault: bool = False):
        self.sim = sim
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text("time | category | message\n", encoding="utf-8")
        self.state = State.IDLE
        self.entered_at = 0.0
        self.motion: Motion | None = None
        self.ball: int | None = None
        self.colour: str | None = None
        self.cycle = 0
        self.completed = 0
        self.inject_vision_fault = inject_vision_fault
        self.fault_injected = False
        self.fault_reason = ""

        self.p1 = sim.getObject("/Picker1/target")
        self.p2 = sim.getObject("/Picker2/target")
        self.tip1 = sim.getObject("/Picker1/tip")
        self.tip2 = sim.getObject("/Picker2/tip")
        self.camera = sim.getObject("/ColorVisionSensor")
        self.home1 = sim.getObjectPosition(self.p1, sim.handle_world)
        self.home2 = sim.getObjectPosition(self.p2, sim.handle_world)

    def now(self) -> float:
        return self.sim.getSimulationTime()

    def log(self, category: str, message: str) -> None:
        stamp = self.now()
        line = f"{stamp:7.2f} | {category:<10} | {message}"
        print(line)
        with self.log_path.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
        self.sim.addLog(self.sim.verbosity_scriptinfos, f"[cw5] {line}")

    def transition(self, following: State, reason: str) -> None:
        if not can_transition(self.state, following):
            raise RuntimeError(f"Illegal transition: {self.state.name} -> {following.name}")
        previous = self.state
        self.state = following
        self.entered_at = self.now()
        self.motion = None
        self.log("TRANSITION", f"{previous.name} -> {following.name}; {reason}")

    def fail(self, reason: str) -> None:
        self.fault_reason = reason
        self.transition(State.FAULT, reason)
        self.log("FAULT", reason)

    def command_move(self, target: int, destination: list[float], label: str) -> None:
        self.sim.setObjectPosition(target, self.sim.handle_world, destination)
        self.motion = Motion(target, destination)
        self.log("COMMAND", label)

    def motion_done(self, tip: int, tolerance: float = 0.045) -> bool:
        if self.motion is None:
            return False
        actual = self.sim.getObjectPosition(tip, self.sim.handle_world)
        error = sum((actual[i] - self.motion.destination[i]) ** 2 for i in range(3)) ** 0.5
        return error <= tolerance

    def create_ball(self) -> None:
        self.cycle += 1
        self.colour = random.choice(tuple(COLOURS))
        self.ball = self.sim.createPrimitiveShape(
            self.sim.primitiveshape_spheroid, [0.055, 0.055, 0.055], 0
        )
        self.sim.setObjectInt32Param(self.ball, self.sim.shapeintparam_static, 1)
        self.sim.setObjectAlias(self.ball, f"CW5Ball_{self.cycle:02d}_{self.colour}")
        self.sim.setObjectPosition(self.ball, self.sim.handle_world, [-0.78, PICKUP[1], BALL_Z])
        self.sim.setShapeColor(
            self.ball, "", self.sim.colorcomponent_ambient_diffuse, COLOURS[self.colour]
        )
        self.log("EVENT", f"ball #{self.cycle} generated; colour={self.colour}")

    def attach(self, tip: int, robot_name: str) -> None:
        assert self.ball is not None
        self.sim.setObjectParent(self.ball, tip, False)
        self.sim.setObjectPosition(self.ball, tip, [0, 0, -0.06])
        self.log("EVENT", f"{robot_name} grasp confirmed")

    def release(self, position: list[float], robot_name: str) -> None:
        assert self.ball is not None
        self.sim.setObjectParent(self.ball, self.sim.handle_world, True)
        self.sim.setObjectPosition(self.ball, self.sim.handle_world, position)
        self.log("EVENT", f"{robot_name} release confirmed")

    def recognise_colour(self) -> str | None:
        """Use the vision sensor as a trigger, then classify the scene colour."""
        self.sim.handleVisionSensor(self.camera)
        if self.inject_vision_fault and not self.fault_injected:
            self.fault_injected = True
            return None
        if self.ball is None:
            return None
        raw_colour = self.sim.getShapeColor(
            self.ball, "", self.sim.colorcomponent_ambient_diffuse
        )
        rgb = self.extract_rgb(raw_colour)
        if rgb is None:
            self.log("FAULT", f"unexpected colour response from API: {raw_colour!r}")
            return None
        return min(COLOURS, key=lambda name: sum((rgb[i] - COLOURS[name][i]) ** 2 for i in range(3)))

    @staticmethod
    def extract_rgb(value) -> list[float] | None:
        """Extract RGB values from CoppeliaSim API return formats.

        CoppeliaSim 4.10 returns the colour as a nested list, for example
        ``[[1.0, 0.05, 0.05]]``.  Older releases can return a flat list.
        """
        if isinstance(value, (list, tuple)):
            if len(value) >= 3 and all(isinstance(component, (int, float)) for component in value[:3]):
                return [float(component) for component in value[:3]]
            for nested in value:
                rgb = SortingController.extract_rgb(nested)
                if rgb is not None:
                    return rgb
        return None

    def timed_out(self) -> bool:
        limit = TIMEOUT.get(self.state)
        return limit is not None and self.now() - self.entered_at > limit

    def tick(self, start: bool, reset: bool) -> None:
        if self.state is State.FAULT:
            if reset:
                self.log("EVENT", f"fault reset accepted: {self.fault_reason}")
                self.transition(State.IDLE, "operator reset")
            return

        if self.timed_out():
            self.fail(f"timeout in {self.state.name}")
            return

        if self.state is State.IDLE:
            if start:
                self.transition(State.SPAWN, "start command")

        elif self.state is State.SPAWN:
            self.create_ball()
            self.transition(State.FEED, "ball is ready on conveyor")

        elif self.state is State.FEED:
            assert self.ball is not None
            q = min(1.0, (self.now() - self.entered_at) / 1.8)
            x = -0.78 + (PICKUP[0] + 0.78) * q
            self.sim.setObjectPosition(self.ball, self.sim.handle_world, [x, PICKUP[1], BALL_Z])
            if q >= 1.0:
                self.transition(State.P1_APPROACH, "ball reached pickup zone")

        elif self.state is State.P1_APPROACH:
            if self.motion is None:
                self.command_move(self.p1, [*PICKUP, SAFE_Z], "Picker1: approach pickup zone")
            elif self.motion_done(self.tip1):
                self.transition(State.P1_GRASP, "Picker1 reached pickup point")

        elif self.state is State.P1_GRASP:
            if self.motion is None:
                self.command_move(self.p1, [*PICKUP, GRASP_Z], "Picker1: lower for grasp")
            elif self.motion_done(self.tip1):
                self.attach(self.tip1, "Picker1")
                self.transition(State.P1_TRANSFER, "Picker1 grasped ball")

        elif self.state is State.P1_TRANSFER:
            if self.motion is None:
                self.command_move(self.p1, [*TABLE, SAFE_Z], "Picker1: transfer ball to table")
            elif self.motion_done(self.tip1):
                self.transition(State.P1_RELEASE, "Picker1 reached table")

        elif self.state is State.P1_RELEASE:
            if self.motion is None:
                self.command_move(self.p1, [*TABLE, GRASP_Z], "Picker1: lower at table")
            elif self.motion_done(self.tip1):
                self.release([*TABLE, BALL_Z], "Picker1")
                self.transition(State.P1_RETURN, "ball placed on table")

        elif self.state is State.P1_RETURN:
            if self.motion is None:
                self.command_move(self.p1, self.home1, "Picker1: return home")
            elif self.motion_done(self.tip1):
                self.transition(State.VISION, "Picker1 is home")

        elif self.state is State.VISION:
            if self.now() - self.entered_at >= 0.4:
                recognised = self.recognise_colour()
                if recognised is None:
                    self.fail("vision sensor did not identify a ball colour")
                else:
                    self.colour = recognised
                    self.log("EVENT", f"vision result accepted; colour={recognised}")
                    self.transition(State.P2_APPROACH, "vision result received")

        elif self.state is State.P2_APPROACH:
            if self.motion is None:
                self.command_move(self.p2, [*TABLE, SAFE_Z], "Picker2: approach table")
            elif self.motion_done(self.tip2):
                self.transition(State.P2_GRASP, "Picker2 reached table")

        elif self.state is State.P2_GRASP:
            if self.motion is None:
                self.command_move(self.p2, [*TABLE, GRASP_Z], "Picker2: lower for grasp")
            elif self.motion_done(self.tip2):
                self.attach(self.tip2, "Picker2")
                self.transition(State.P2_TRANSFER, "Picker2 grasped ball")

        elif self.state is State.P2_TRANSFER:
            assert self.colour is not None
            if self.motion is None:
                x, y, _ = BINS[self.colour]
                self.command_move(self.p2, [x, y, SAFE_Z], f"Picker2: move to {self.colour} bin")
            elif self.motion_done(self.tip2):
                self.transition(State.P2_RELEASE, "Picker2 reached selected bin")

        elif self.state is State.P2_RELEASE:
            assert self.colour is not None
            x, y, z = BINS[self.colour]
            if self.motion is None:
                self.command_move(self.p2, [x, y, z], "Picker2: lower into bin")
            elif self.motion_done(self.tip2):
                self.release([x, y, z], "Picker2")
                self.transition(State.RETURN, "ball sorted")

        elif self.state is State.RETURN:
            if self.motion is None:
                self.command_move(self.p2, self.home2, "Picker2: return home")
            elif self.motion_done(self.tip2):
                self.completed += 1
                self.log("EVENT", f"cycle {self.completed} completed")
                self.transition(State.SPAWN, "next cycle")


def main() -> None:
    parser = argparse.ArgumentParser(description="CW5 two-robot FSM controller")
    parser.add_argument("--cycles", type=int, default=3, help="number of completed cycles")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument(
        "--log",
        default="logs/cw5_events.log",
        help="event-log path relative to the laboratory folder",
    )
    parser.add_argument("--inject-vision-fault", action="store_true")
    parser.add_argument("--auto-reset", action="store_true")
    parser.add_argument(
        "--stop-after-recovery",
        action="store_true",
        help="finish after FAULT, RESET and the beginning of the next cycle",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    log_path = Path(args.log)
    if not log_path.is_absolute():
        log_path = root / log_path
    client = RemoteAPIClient("localhost", args.port)
    sim = client.require("sim")
    controller = SortingController(
        sim,
        log_path,
        inject_vision_fault=args.inject_vision_fault,
    )

    client.setStepping(True)
    sim.startSimulation()
    reset_at = None
    try:
        while controller.completed < args.cycles:
            reset = False
            if controller.state is State.FAULT and args.auto_reset:
                reset_at = reset_at or controller.now() + 1.0
                reset = controller.now() >= reset_at
            controller.tick(start=True, reset=reset)
            if (
                args.stop_after_recovery
                and controller.fault_injected
                and controller.state is State.SPAWN
            ):
                break
            client.step()
    finally:
        sim.stopSimulation()


if __name__ == "__main__":
    main()
