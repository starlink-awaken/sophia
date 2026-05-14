"""Tests for Sophia paradigm compiler."""
import pytest
from sophia.compiler import compile_paradigm_sync, recompile_from_dict


class TestCompileParadigmSync:
    def test_comparative(self):
        prog = compile_paradigm_sync("Compare Python vs Go")
        op_names = [o.value for o in prog.operations]
        assert "compare" in op_names

    def test_problem_solving(self):
        prog = compile_paradigm_sync("Why does PostgreSQL deadlock?")
        op_names = [o.value for o in prog.operations]
        assert "hypothesize" in op_names
        assert "eliminate" in op_names

    def test_survey(self):
        prog = compile_paradigm_sync("Survey AI agents 2026")
        op_names = [o.value for o in prog.operations]
        assert "synthesize" in op_names

    def test_default(self):
        prog = compile_paradigm_sync("How does deep learning work?")
        ops = [o.value for o in prog.operations]
        assert "decompose" in ops
        assert "search" in ops
        assert "verify" in ops
        assert "conclude" in ops

    def test_empty_query_raises(self):
        with pytest.raises(ValueError):
            compile_paradigm_sync("")
        with pytest.raises(ValueError):
            compile_paradigm_sync("   ")

    def test_program_is_valid(self):
        prog = compile_paradigm_sync("Compare Rust vs Go")
        issues = prog.validate()
        assert issues == []


class TestRecompileFromDict:
    def test_with_query(self):
        prog = compile_paradigm_sync("Compare A vs B")
        d = prog.to_dict(include_query="Compare A vs B")
        prog2 = recompile_from_dict(d)
        assert prog2.name == prog.name
        assert len(prog2.operations) == len(prog.operations)

    def test_without_query(self):
        prog = compile_paradigm_sync("Test query")
        d = prog.to_dict()
        prog2 = recompile_from_dict(d)
        assert prog2.name == "Adaptive Research"
