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
            ### Answer competency questions (see README) ###############################
            (
                f"<{abox}_System01> sms:realizes ?cos. ?i sms:represents ?cos",
                ["_Model01"],
            ),  # CQ 2a
            (
                (
                    f"<{abox}_System01> sms:realizes ?cos. ?m sms:represents ?cos."
                    "?i sms:instanceOf ?m"
                ),
                ["_ModelInstance01"],
            ),  # CQ 2b
            (
                f"<{abox}_Model01> sms:hasParameter ?i. ?i rdf:type sms:ModelParameterFree",
                ["_Model01_Parameter01", "_Model01_Parameter02"],
            ),  # CQ 3a
            (
                f"<{abox}_Model01> sms:hasParameter ?i. ?i rdf:type sms:ModelParameterDefault",
                ["_Model01_Parameter00"],
            ),  # CQ 3b
            (
                f"<{abox}_Solver01> sms:hasSetting ?i. ?i rdf:type sms:SolverSettingFree",
                ["_Solver01_Setting01"],
            ),  # CQ 5a
            (
                f"<{abox}_Solver01> sms:hasSetting ?i. ?i rdf:type sms:SolverSettingDefault",
                ["_Solver01_Setting00"],
            ),  # CQ 5b
            # ...
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
