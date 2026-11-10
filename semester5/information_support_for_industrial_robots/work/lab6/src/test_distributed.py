"""Integration checks for the distributed controller demo."""

from pathlib import Path

from main import run_demo


def main() -> None:
    log_path = Path(__file__).resolve().parents[1] / "logs" / "test_integration.log"
    summary = run_demo(
        cycles=2,
        endpoint="tcp://127.0.0.1:24061",
        log_path=log_path,
        run_tests=True,
    )

    assert summary.normal_cycles == 3
    assert summary.device_fault_detected
    assert summary.link_loss_detected
    assert summary.delayed_ack_detected
    assert summary.duplicate_blocked
    assert summary.restart_completed
    print("Distributed integration tests: OK")


if __name__ == "__main__":
    main()
