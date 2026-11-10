"""Distributed controller demo for the two-robot sorting cell.

The coordinator and local controllers run in separate processes and exchange
versioned JSON messages over ZeroMQ TCP.  The same interfaces can be connected
to the CoppeliaSim objects from the Lab 5 scene.
"""

from __future__ import annotations

import argparse
import itertools
import logging
import multiprocessing as mp
import time
from dataclasses import dataclass, field
from pathlib import Path

import zmq

from controller import controller_process
from protocol import Message, command


COMPONENTS = ("conveyor", "picker1", "vision", "picker2")
DEFAULT_ENDPOINT = "tcp://127.0.0.1:24060"


@dataclass(slots=True)
class TestSummary:
    normal_cycles: int = 0
    device_fault_detected: bool = False
    link_loss_detected: bool = False
    delayed_ack_detected: bool = False
    duplicate_blocked: bool = False
    restart_completed: bool = False
    events: list[str] = field(default_factory=list)


class Coordinator:
    def __init__(self, endpoint: str, log_path: Path) -> None:
        self.endpoint = endpoint
        self.started_at = time.monotonic()
        self.sequence = itertools.count(1)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(endpoint)
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.last_seen: dict[str, float] = {}
        self.inbox: list[Message] = []
        self.summary = TestSummary()

        log_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(f"cw6-{id(self)}")
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        formatter = logging.Formatter("%(message)s")
        file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        stream_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def log(self, component: str, operation_id: str, category: str, text: str) -> None:
        elapsed = time.monotonic() - self.started_at
        line = f"{elapsed:6.2f} | {component:11} | {operation_id:9} | {category:10} | {text}"
        self.logger.info(line)
        self.summary.events.append(line)

    def close(self) -> None:
        for handler in self.logger.handlers:
            handler.close()
        self.socket.close(0)
        self.context.term()

    def _send(self, target: str, message: Message) -> None:
        self.socket.send_multipart([target.encode("utf-8"), message.encode()])
        self.log(target, message.operation_id or "-", "TX", message.command or message.kind)

    def _receive_once(self, timeout_ms: int) -> Message | None:
        if not dict(self.poller.poll(timeout_ms)):
            return None
        route, raw = self.socket.recv_multipart()
        message = Message.decode(raw)
        component = route.decode("utf-8")
        self.last_seen[component] = time.monotonic()
        if message.kind != "HEARTBEAT":
            self.log(component, message.operation_id or "-", message.kind, message.status)
        return message

    def wait_ready(self, timeout: float = 3.0) -> None:
        ready: set[str] = set()
        deadline = time.monotonic() + timeout
        while ready != set(COMPONENTS):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"Controllers did not start: {sorted(set(COMPONENTS) - ready)}")
            message = self._receive_once(int(remaining * 1000))
            if message and message.kind == "HELLO":
                ready.add(message.component)
        self.log("coordinator", "-", "SYSTEM", "all controllers READY")

    def execute(
        self,
        target: str,
        name: str,
        *,
        operation_id: str | None = None,
        ack_timeout: float = 0.50,
        result_timeout: float = 1.50,
        **payload: object,
    ) -> Message:
        operation_id = operation_id or f"op-{next(self.sequence):04d}"
        self._send(target, command(target, operation_id, name, **payload))

        ack_deadline = time.monotonic() + ack_timeout
        result_deadline: float | None = None
        while True:
            deadline = result_deadline if result_deadline is not None else ack_deadline
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                phase = "RESULT" if result_deadline is not None else "ACK"
                raise TimeoutError(f"{target} {phase} timeout for {operation_id}")

            message = self._receive_once(max(1, int(remaining * 1000)))
            if message is None:
                continue
            if message.operation_id != operation_id:
                self.inbox.append(message)
                continue
            if message.kind == "RESULT":
                return message
            if message.kind == "ACK":
                result_deadline = time.monotonic() + result_timeout

    def run_cycle(self, cycle: int) -> None:
        self.execute("conveyor", "FEED_BALL", cycle=cycle)
        self.execute("picker1", "MOVE_TO_TABLE", cycle=cycle)
        vision = self.execute("vision", "CLASSIFY", cycle=cycle)
        if vision.status != "DONE":
            raise RuntimeError("Vision subsystem failed")
        colour = str(vision.payload["colour"])
        self.execute("picker2", "SORT_TO_BIN", cycle=cycle, colour=colour)
        self.summary.normal_cycles += 1
        self.log("coordinator", f"cycle-{cycle}", "CYCLE", f"completed; colour={colour}")

    def run_integration_tests(self) -> None:
        # Device failure.
        failed = self.execute("picker2", "SORT_TO_BIN", force_error=True)
        self.summary.device_fault_detected = failed.status == "ERROR"
        self.log("coordinator", failed.operation_id, "TEST", "device fault handled")

        # Loss of communication and subsequent recovery.
        try:
            self.execute("conveyor", "PAUSE_LINK", pause=0.70, result_timeout=0.20)
        except TimeoutError as error:
            self.summary.link_loss_detected = True
            self.log("coordinator", "link-test", "TIMEOUT", str(error))
        time.sleep(0.75)
        recovered = self.execute("conveyor", "RESET")
        self.log("coordinator", recovered.operation_id, "RECOVERY", "link restored")

        # Delayed acknowledgement.
        try:
            self.execute("picker1", "MOVE_TO_TABLE", ack_delay=0.45, ack_timeout=0.15)
        except TimeoutError as error:
            self.summary.delayed_ack_detected = True
            self.log("coordinator", "delay-test", "TIMEOUT", str(error))
        time.sleep(0.50)

        # Repeated command with the same operation ID must not be executed twice.
        duplicate_id = "duplicate-001"
        self.execute("vision", "CLASSIFY", operation_id=duplicate_id, cycle=2)
        duplicate = self.execute("vision", "CLASSIFY", operation_id=duplicate_id, cycle=2)
        self.summary.duplicate_blocked = duplicate.status == "DUPLICATE"
        self.log("coordinator", duplicate_id, "TEST", "duplicate command blocked")

        # Reset and restart after failures.
        for component in COMPONENTS:
            self.execute(component, "RESET")
        self.run_cycle(self.summary.normal_cycles + 1)
        self.summary.restart_completed = True


def run_demo(cycles: int, endpoint: str, log_path: Path, run_tests: bool = True) -> TestSummary:
    stop_event = mp.Event()
    processes = [
        mp.Process(
            target=controller_process,
            args=(component, endpoint, stop_event),
            name=f"cw6-{component}",
        )
        for component in COMPONENTS
    ]
    coordinator = Coordinator(endpoint, log_path)

    try:
        for process in processes:
            process.start()
        coordinator.wait_ready()
        for cycle in range(1, cycles + 1):
            coordinator.run_cycle(cycle)
        if run_tests:
            coordinator.run_integration_tests()
        return coordinator.summary
    finally:
        stop_event.set()
        for process in processes:
            process.join(timeout=1.0)
            if process.is_alive():
                process.terminate()
                process.join(timeout=1.0)
        coordinator.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=3)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument(
        "--log",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "logs" / "integration.log",
    )
    parser.add_argument("--no-tests", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = run_demo(args.cycles, args.endpoint, args.log, not args.no_tests)
    print(
        "SUMMARY",
        {
            "normal_cycles": result.normal_cycles,
            "device_fault": result.device_fault_detected,
            "link_loss": result.link_loss_detected,
            "delayed_ack": result.delayed_ack_detected,
            "duplicate_blocked": result.duplicate_blocked,
            "restart_completed": result.restart_completed,
        },
    )
