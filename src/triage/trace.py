"""Execution trace: every pipeline stage records what it did and how long it took."""

from __future__ import annotations

import time
from contextlib import contextmanager

from triage.models import TraceStep


class Trace:
    def __init__(self) -> None:
        self.steps: list[TraceStep] = []

    @contextmanager
    def step(self, name: str):
        t0 = time.perf_counter()
        holder = {"detail": ""}
        try:
            yield holder
        finally:
            self.steps.append(
                TraceStep(
                    step=name,
                    detail=holder["detail"],
                    ms=round((time.perf_counter() - t0) * 1000, 1),
                )
            )
