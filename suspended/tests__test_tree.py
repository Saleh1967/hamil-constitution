# -*- coding: utf-8 -*-
"""Tests for SLGE-SEED — the knowledge tree as an SLGE engine (الحامل)."""
import importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("slge_seed", ROOT / "src" / "slge" / "slge_seed.py")
tr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)


def test_tr1_tree_loads_with_roots():
    tree = tr.load_tree()
    assert len(tree["nodes"]) >= 14
    assert any(n["genus"] == "جذر" for n in tree["nodes"])


def test_tr5_bit_address_cells():
    a = tr.bit_address("يَا أَيُّهَا الَّذِينَ آمَنُوا إِذَا نُودِيَ لِلصَّلَاةِ")
    cells = a["cells"]
    assert len(cells) >= 3 and all(1 <= c <= 114 for c in cells)
    assert tr.bit_address("في")["missing_letters"] == []
    assert tr.bit_address("پاک")["missing_letters"]
    n = next(n for n in tr.load_tree()["nodes"] if n["id"] == "N-ASMA")
    a = tr.address_node(n)
    assert a["kind"] == "bits" and len(a["cells"]) >= 3


def test_tr4_book_nodes_verified():
    for n in tr.load_tree()["nodes"]:
        if n["source"]["kind"] == "book":
            assert tr.address_node(n)["verified"] is True


def test_tr7_bit_retrieval():
    res = tr.retrieve("ما الخاصية التي أحراقها في النار")
    assert res and res[0][0] == "N-QADR"


def test_tr7_word_retrieval():
    res = tr.retrieve("ما هي الغريزة والتدين")
    assert any(i == "N-GR-TADAYYUN" for i, _, _ in res)


def test_engine_self_check():
    assert tr.main() == 0
