"""Message contract for the distributed sorting-cell controllers."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Message:
    kind: str
    component: str
    operation_id: str = ""
    command: str = ""
    status: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def encode(self) -> bytes:
        return json.dumps(asdict(self), ensure_ascii=False).encode("utf-8")

    @classmethod
    def decode(cls, raw: bytes) -> "Message":
        data = json.loads(raw.decode("utf-8"))
        return cls(**data)


def command(component: str, operation_id: str, name: str, **payload: Any) -> Message:
    return Message(
        kind="COMMAND",
        component=component,
        operation_id=operation_id,
        command=name,
        payload=payload,
    )
