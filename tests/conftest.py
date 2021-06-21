#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Provide global test fixtures for unit tests."""

import os

import pytest


@pytest.fixture
def kb(tmp_path):
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
        "owl:imports <https://ontologies.msaas.me/ms-aas-ontology.ttl> .",
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
