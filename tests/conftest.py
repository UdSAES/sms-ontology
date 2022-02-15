#!/usr/bin/env python3
# -*- coding: utf8 -*-

# SPDX-FileCopyrightText: 2022 UdS AES <https://www.uni-saarland.de/lehrstuhl/frey.html>
# SPDX-License-Identifier: MIT


"""Provide global test fixtures for unit tests."""

import os

import pytest
import rdflib
import yaml
from jinja2 import Environment, FileSystemLoader
from rdflib.namespace import OWL, RDF, NamespaceManager

ENV = Environment(
    loader=FileSystemLoader(
        os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    ),
    trim_blocks=True,
    lstrip_blocks=True,
)


@pytest.fixture
def tbox_rbox():
    """Retrieve the full path to the file defining TBox and RBox."""

    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "sms-ontology.ttl")
    )

    return path


@pytest.fixture
def abox():
    """Retrieve the full path to the file containing the definition of the ABox."""

    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "data", "individuals.ttl")
    )

    return path


@pytest.fixture
def kb(tmp_path, hermit, tbox_rbox):
    """Retrieve the full path to the file containing the knowledge base (KB)."""

    file_name = "individuals.ttl"
    file_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "data", file_name)
    )

    file_path_new = os.path.join(tmp_path, file_name)

    # Point to local version of TBox/RBox instead of web resource
    with open(file_path, "r") as fp:
        content = fp.read()

    content = content.replace(
        f"owl:imports <https://purl.org/sms-ontology> .",
        f"owl:imports <file://{tbox_rbox}> .",
    )

    with open(file_path_new, "w") as fp:
        fp.write(content)

    return file_path_new


@pytest.fixture
def hermit():
    """Retrieve the command for using the HermiT reasoner."""

    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "HermiT", "HermiT.jar")
    )

    return f"java -jar {path}"


def pytest_generate_tests(metafunc):
    """Parameterize tests by reading their consituents from a YAML-file."""

    # Load questions from rendered template
    template = ENV.get_template("tests/questions.yaml.j2")
    collection = yaml.full_load(
        template.render(prefix="https://ontologies.msaas.me/individuals-test.ttl#")
    )

    # Generate tests using the hook provided by pytest
    if "questions_competency" in metafunc.fixturenames:
        metafunc.parametrize("questions_competency", collection["competency"])


@pytest.fixture
def individuals_all():
    """Return path to .ttl-file containing _all_ triples."""

    path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), "data", "individuals_with_reasoning.ttl"
        )
    )

    return path


@pytest.fixture
def graph_empty():
    """Provide an empty graph that has all the necessary prefix-bindings."""

    graph = rdflib.Graph()

    graph.bind("rdf", RDF)
    graph.bind("owl", OWL)
    graph.bind("sms", rdflib.Namespace("https://purl.org/sms-ontology#"))

    return graph
