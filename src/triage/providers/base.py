"""DecisionProvider: turns the safe part of a free-text request into typed Criteria. Nothing else."""

from __future__ import annotations

from typing import Protocol

from triage.models import Criteria


class DecisionProvider(Protocol):
    name: str

    def parse(self, text: str, default_weights: dict[str, float]) -> Criteria: ...
