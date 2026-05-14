"""Tests for Sophia symbol system."""
from sophia.symbols import (
    AtomicOp, ResearchState, ParadigmProgram, TransitionRule,
    gate_always, gate_has_sources, gate_has_entities,
    gate_has_contradictions, gate_quality_pass, BASE_TRANSITIONS,
)


class TestAtomicOp:
    def test_from_string_lowercase(self):
        assert AtomicOp.from_string("decompose") == AtomicOp.DECOMPOSE
        assert AtomicOp.from_string("search") == AtomicOp.SEARCH
        assert AtomicOp.from_string("verify") == AtomicOp.VERIFY

    def test_from_string_uppercase(self):
        assert AtomicOp.from_string("DECOMPOSE") == AtomicOp.DECOMPOSE
        assert AtomicOp.from_string("CONCLUDE") == AtomicOp.CONCLUDE

    def test_from_string_invalid(self):
        assert AtomicOp.from_string("nonexistent") is None


class TestGates:
    def test_gate_has_sources(self):
        assert gate_has_sources({"source_count": 5}) is True
        assert gate_has_sources({"source_count": 1}) is False
        assert gate_has_sources({}) is False

    def test_gate_has_entities(self):
        assert gate_has_entities({"entity_count": 1}) is True
        assert gate_has_entities({"entity_count": 0}) is False

    def test_gate_quality_pass(self):
        assert gate_quality_pass({"quality_score": 80}) is True
        assert gate_quality_pass({"quality_score": 40}) is False

    def test_gate_always(self):
        assert gate_always({}) is True


class TestParadigmProgram:
    def test_validate_empty(self):
        p = ParadigmProgram(name="empty")
        issues = p.validate()
        assert len(issues) >= 2

    def test_validate_valid(self):
        ops = [AtomicOp.DECOMPOSE, AtomicOp.SEARCH, AtomicOp.VERIFY]
        transitions = [t for t in BASE_TRANSITIONS if t.operation in ops]
        p = ParadigmProgram(name="test", operations=ops, transitions=transitions)
        assert p.validate() == []

    def test_to_dict(self):
        ops = [AtomicOp.DECOMPOSE, AtomicOp.SEARCH]
        p = ParadigmProgram(name="test", operations=ops)
        d = p.to_dict(include_query="test query")
        assert d["name"] == "test"
        assert "test query" in d["query"]
        assert len(d["ops"]) == 2

    def test_from_dict(self):
        d = {"name": "test", "ops": ["decompose", "search"]}
        p = ParadigmProgram.from_dict(d)
        assert p.name == "test"
        assert len(p.operations) == 2

    def test_to_mermaid(self):
        ops = [AtomicOp.DECOMPOSE, AtomicOp.SEARCH]
        transitions = [t for t in BASE_TRANSITIONS if t.operation in ops]
        p = ParadigmProgram(name="test", operations=ops, transitions=transitions)
        m = p.to_mermaid()
        assert m.startswith("stateDiagram-v2")
        assert "decompose" in m

    def test_diff(self):
        ops = [AtomicOp.DECOMPOSE, AtomicOp.CONCLUDE]
        p1 = ParadigmProgram(name="a", operations=ops, transitions=[])
        p2 = ParadigmProgram(name="b", operations=[AtomicOp.DECOMPOSE, AtomicOp.SEARCH], transitions=[])
        delta = p1.diff(p2)
        assert delta["added_ops"] == ["search"]
        assert delta["removed_ops"] == ["conclude"]
        assert delta["common_ops"] == ["decompose"]


class TestBaseTransitions:
    def test_transition_count(self):
        assert len(BASE_TRANSITIONS) >= 13

    def test_all_ops_have_transitions(self):
        op_set = {t.operation for t in BASE_TRANSITIONS}
        assert AtomicOp.DECOMPOSE in op_set
        assert AtomicOp.CONCLUDE in op_set
