#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Query ontology for answers to competency questions using HermiT reasoner."""

import invoke
import pytest


class TestCompetency(object):
    def test_satisfiability(self, hermit, kb):
        """Verify that the knowledge base is satisfiable/consistent (has a model)."""

        ctx = invoke.context.Context()
        cmd = f"{hermit} --consistency {kb}"

        result = ctx.run(cmd)
        satisfiable = (
            True if result.ok and ("is satisfiable" in result.stdout) else False
        )

        assert satisfiable
