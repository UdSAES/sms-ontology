#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Query ontology for answers to competency questions using HermiT reasoner."""

import json
import os

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

    @pytest.mark.parametrize(
        "query, expected",
        [
            ("query_all.ttl", None),
            ("01.ttl", "01.json"),
        ],
    )
    def test_instance_retrieval(self, kb, query, expected):
        """Verify that individuals in ABox are found as expected."""

        # Load files in insanely verbose manner
        query_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "queries", query)
        )

        with open(query_path, "r") as fp:
            query = fp.read()

        if expected != None:
            expected_path = os.path.normpath(
                os.path.join(os.path.dirname(__file__), "expectations", expected)
            )

            with open(expected_path, "r") as fp:
                data = fp.read()

            expected = json.loads(data)

        # Parse graph
        graph = rdflib.Graph()
        graph.parse(kb, format="turtle")

        answer = graph.query(query)

        actual = []

        # Careful, assumes that SPARQL-query `SELECT`s exactly three variables!
        for subject, predicate, object in answer:
            actual.append(object.n3())

            print(f"\n{subject}\n--- {predicate}\n----- {object}")

        if expected != None:
            assert [x in actual for x in expected] if actual != [] else False
