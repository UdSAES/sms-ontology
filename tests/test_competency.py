#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Query ontology for answers to competency questions using HermiT reasoner."""

import invoke
import pytest
import rdflib


class TestCompetency(object):
    abox = "https://ontologies.msaas.me/individuals-test.ttl#"  # prefix for ABox

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
        "where, expected",
        [
            ### Verify that roles work as expected (explicit relations only) ###########
            (f"?i sms:instanceOf <{abox}_Model01>", ["_ModelInstance01"]),
        ],
    )
    def test_instance_retrieval(self, kb, ns_mgr, where, expected):
        """Verify that individuals in ABox are found as expected."""

        # Load knowledge base as graph, using common prefixes via namespace manager
        graph = rdflib.Graph()
        graph.namespace_manager = ns_mgr
        graph.parse(kb, format="turtle")

        # Prepare and execute query
        query = f"SELECT ?i WHERE {{ {where} }}"
        answer = graph.query(query)

        actual = []
        for individual in answer:
            actual.append(individual)

        assert [x in actual for x in expected] if actual != [] else False
