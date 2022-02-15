#!/usr/bin/env python3
# -*- coding: utf8 -*-

# SPDX-FileCopyrightText: 2022 UdS AES <https://www.uni-saarland.de/lehrstuhl/frey.html>
# SPDX-License-Identifier: MIT


"""Query ontology for answers to competency questions using HermiT reasoner."""

import invoke
import pytest
import rdflib


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

    def test_sparql_select(self, questions_competency, individuals_all, graph_empty):
        graph = graph_empty.parse(individuals_all, format="turtle")

        a0 = graph.query(questions_competency["query"])

        # Construct list of expected literal values
        actual = []
        for row in a0:
            actual.append([item.n3() for item in row])

        # Verify that each expected result is in the list of actual results
        assert questions_competency["expected"] == actual
