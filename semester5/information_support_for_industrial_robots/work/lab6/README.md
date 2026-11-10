# Computer practical work 6

The sorting cell is controlled by a coordinator and four local components:
`conveyor`, `picker1`, `vision`, and `picker2`.  Each component runs in a
separate process.  ZeroMQ TCP transports versioned JSON messages containing a
component identifier, operation ID, command, status, payload, and timestamp.

Run the full demonstration from the `lab6` directory:

```bash
python src/main.py --cycles 3
```

Run the repeatable integration checks:

```bash
python src/test_distributed.py
```

The CoppeliaSim scene is stored in `src/main.ttt`.  The local controllers are
implemented as test models, which lets communication failures and duplicate
commands be tested deterministically without damaging the scene.
