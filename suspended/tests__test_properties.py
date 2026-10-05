# -*- coding: utf-8 -*-
"""اختبارات خصائص — بذر ثابت، مكتبة قياسية (النظير التطبيقي لبراهين Lean)."""
import importlib.util, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("slge_seed", ROOT / "src" / "slge" / "slge_seed.py")
tr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)
random.seed(116)


def test_bit_address_deterministic():
    for _ in range(50):
        w = random.choice(["نار", "قامة", "نجاد", "سماء", "أرض", "علم"])
        assert tr.bit_address(w) == tr.bit_address(w)


def test_cells_bounded_1_114():
    for _ in range(100):
        w = random.choice(["نارٍ", "قامةٌ", "نجادِ", "بسم", "علمٌ", "السماء"])
        for c in tr.bit_address(w)["cells"]:
            assert 1 <= c <= 114


def test_quran_nodes_cells_within_constitution():
    tree = tr.load_tree()
    for n in tree["nodes"]:
        if n["source"]["kind"] == "quran":
            for c in tr.address_node(n)["cells"]:
                assert 1 <= c <= 114


def test_tree_acyclic():
    tree = tr.load_tree()
    ids = {n["id"]: n for n in tree["nodes"]}
    for n in tree["nodes"]:
        seen = set()
        cur = n
        while cur["parents"]:
            pid = cur["parents"][0]
            assert pid not in seen, "دورة!"
            seen.add(pid)
            cur = ids[pid]
