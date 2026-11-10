"""Reusable ZeroMQ worker process representing a local controller."""

from __future__ import annotations

import time
from dataclasses import dataclass
from multiprocessing.synchronize import Event
from typing import Any

import zmq

from protocol import Message


@dataclass(slots=True)
class PendingOperation:
    operation_id: str
    command: str
    payload: dict[str, Any]
    finish_at: float
    ack_at: float
    ack_sent: bool = False


def _result_payload(identity: str, operation: PendingOperation) -> dict[str, Any]:
    if identity == "vision":
        colours = ("red", "green", "blue")
        cycle = int(operation.payload.get("cycle", 1))
        return {"colour": colours[(cycle - 1) % len(colours)], "confidence": 0.97}
    return {"command": operation.command, "completed": True}


def controller_process(
    identity: str,
    endpoint: str,
    stop_event: Event,
    operation_time: float = 0.12,
) -> None:
    """Run one local controller with ACK, heartbeat and idempotency support."""

    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.setsockopt(zmq.IDENTITY, identity.encode("utf-8"))
    socket.connect(endpoint)
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    completed: dict[str, Message] = {}
    pending: list[PendingOperation] = []
    paused_until = 0.0
    next_heartbeat = 0.0

    socket.send(Message(kind="HELLO", component=identity, status="READY").encode())

    try:
        while not stop_event.is_set():
            now = time.monotonic()
            communication_enabled = now >= paused_until

            if communication_enabled and now >= next_heartbeat:
                socket.send(Message(kind="HEARTBEAT", component=identity, status="ALIVE").encode())
                next_heartbeat = now + 0.20

            if communication_enabled:
                for operation in pending[:]:
                    if not operation.ack_sent and now >= operation.ack_at:
                        socket.send(
                            Message(
                                kind="ACK",
                                component=identity,
                                operation_id=operation.operation_id,
                                command=operation.command,
                                status="ACCEPTED",
                            ).encode()
                        )
                        operation.ack_sent = True

                    if now >= operation.finish_at and operation.ack_sent:
                        status = "ERROR" if operation.payload.get("force_error") else "DONE"
                        result = Message(
                            kind="RESULT",
                            component=identity,
                            operation_id=operation.operation_id,
                            command=operation.command,
                            status=status,
                            payload=(
                                {"error_code": "DEVICE_FAULT"}
                                if status == "ERROR"
                                else _result_payload(identity, operation)
                            ),
                        )
                        completed[operation.operation_id] = result
                        socket.send(result.encode())
                        pending.remove(operation)

            events = dict(poller.poll(20))
            if socket not in events:
                continue

            request = Message.decode(socket.recv())
            if request.kind != "COMMAND":
                continue

            if request.command == "SHUTDOWN":
                socket.send(
                    Message(
                        kind="ACK",
                        component=identity,
                        operation_id=request.operation_id,
                        command=request.command,
                        status="STOPPING",
                    ).encode()
                )
                break

            if request.operation_id in completed:
                previous = completed[request.operation_id]
                socket.send(
                    Message(
                        kind="RESULT",
                        component=identity,
                        operation_id=request.operation_id,
                        command=request.command,
                        status="DUPLICATE",
                        payload={"original_status": previous.status, **previous.payload},
                    ).encode()
                )
                continue

            ack_delay = float(request.payload.get("ack_delay", 0.0))
            duration = float(request.payload.get("duration", operation_time))
            operation = PendingOperation(
                operation_id=request.operation_id,
                command=request.command,
                payload=request.payload,
                ack_at=now + ack_delay,
                finish_at=now + max(duration, ack_delay + 0.02),
            )
            pending.append(operation)

            if request.command == "PAUSE_LINK":
                # Simulate a silent communication channel before ACK/RESULT.
                operation.ack_at = now
                operation.finish_at = now + float(request.payload.get("pause", 0.8)) + 0.02
                paused_until = now + float(request.payload.get("pause", 0.8))
    finally:
        socket.close(0)
        context.term()
