#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Provide global test fixtures for unit tests."""

import os

import pytest
import rdflib
from rdflib.namespace import OWL, RDF, NamespaceManager


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
        f"owl:imports <https://ontologies.msaas.me/sms-ontology.ttl> .",
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


@pytest.fixture
def ns_mgr():
    """Retrieve initialized namespace manager for use with rdflib."""

    ns_mgr = NamespaceManager(rdflib.Graph())

    ns_mgr.bind("rdf", RDF)
    ns_mgr.bind("owl", OWL)
    ns_mgr.bind(
        "sms", rdflib.Namespace("https://ontologies.msaas.me/sms-ontology.ttl#")
    )

    return ns_mgr
