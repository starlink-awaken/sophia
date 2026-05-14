"""Sophia — Symbolic Research Paradigm Engine.

A formal system for composing, compiling, and evolving research paradigms.
Research is modeled as a finite state machine with atomic operations.

Quick start:
    from sophia import compile_paradigm_sync
    program = compile_paradigm_sync("Compare Rust vs Go")
    print(program.to_dict())
"""

from sophia.symbols import (
    AtomicOp,
    BASE_TRANSITIONS,
    ParadigmProgram,
    ResearchState,
    TransitionRule,
    gate_always,
    gate_has_contradictions,
    gate_has_entities,
    gate_has_sources,
    gate_quality_pass,
)
from sophia.compiler import compile_paradigm, compile_paradigm_sync, recompile_from_dict
from sophia.learner import ParadigmLearner, ResearchTrace

__all__ = [
    "AtomicOp", "ResearchState", "TransitionRule", "ParadigmProgram",
    "BASE_TRANSITIONS",
    "gate_always", "gate_has_sources", "gate_has_entities",
    "gate_has_contradictions", "gate_quality_pass",
    "compile_paradigm", "compile_paradigm_sync", "recompile_from_dict",
    "ParadigmLearner", "ResearchTrace",
]
