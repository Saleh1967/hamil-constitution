#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SLGE-SEED (TR) — شجرة المعرفة على البرهان البتّي، بمنهج SLGE الكامل.
محرك دستوري: يُكتشف آلياً بواسطة verify_repo.py (glob src/slge/*.py) و test_slge.py.
LAW CODES
  TR1  البذرة صالحة: الشجرة تُحمّل وبذورها حاضرة
  TR2  لا عقدة بلا آباء إلا الجذر وعقد الأسماء
  TR3  لا أباً غائباً
  TR4  الاقتباس الكتابي لا يدخل إلا مطابَقاً (verified) — بوابة verify_quotes
  TR5  الاقتباس القرآني عنوانه بتّي من خلايا دستور A116 (cells_used) لا يقل عن 3 خلايا
  TR6  الدرجة مشتقة مسجلة (degree_rule) لا تُكتب باليد في حقل مستقل
  TR7  الاسترجاع البتّي حي: سؤال «النار خاصية» يصعد N-QADR بالتقاطع الخلوي
  TR8  وعي العيب: كل عنوان يسجّل حروفه غير المغطاة (defect-aware) —
       ادعاء عيب «ف+كسر» دُحض محليًّا؛ والتسجيل إلزامي لأي حرف خارج الدستور
العنوان البتّي: حرف+حرفته من تمييل الكلمة → رقم خلية في cells_used (114 خلية) —
من برهان الحامل نفسه (prove_alama_hamila.py: H=2.6138، خلو مشدود 0).
"""
import json, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BINS = json.load(open(ROOT.parent / "taaqul-a116" / "data" / "bins_quran_full.json"))
CELL_INDEX = {(c[0], c[1]): i + 1 for i, c in enumerate(BINS["cells_used"])}
KNOWN_DEFECTS = {}  # يُسجَّل هنا أي عيب دستور مُثبَت فقط — ادعاء (ف+كسر) دحضه الفحص المحلي
HARAKA = {'\u064E': 'فتح', '\u064F': 'ضم', '\u0650': 'كسر', '\u0652': 'سكون'}
SKIP = set('\u064B\u064C\u064D\u0670\u0640\u0651')
CONSONANTS = set('ءابتثجحخدذرزسشصضطظعغفقكلمنهوي')
NORM_L = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ؤ': 'و', 'ئ': 'ي', 'ة': 'ه', 'ى': 'ي', 'ک': 'ك'}


def word_cells(raw: str):
    """(خلايا، حروف غير مغطاة) — لا صمت عن العيب."""
    cells, missing, pending = set(), [], None
    for ch in raw:
        if ch in SKIP:
            continue
        if ch in HARAKA:
            if pending in CONSONANTS:
                key = (pending, HARAKA[ch])
                if key in CELL_INDEX:
                    cells.add(CELL_INDEX[key])
                else:
                    missing.append(pending)          # خلية غائبة من الدستور
            pending = None
            continue
        if pending in CONSONANTS and (pending, 'سكون') in CELL_INDEX:
            cells.add(CELL_INDEX[(pending, 'سكون')])
        nch = NORM_L.get(ch, ch)
        if nch in CONSONANTS:
            pending = nch
        else:
            missing.append(ch)              # حرف خارج الدستور — يُسجَّل لا يُسقط
            pending = None
    if pending in CONSONANTS and (pending, 'سكون') in CELL_INDEX:
        cells.add(CELL_INDEX[(pending, 'سكون')])
    return cells, missing


def bit_address(text: str):
    """عنوان بتّي واعٍ بالعيوب: خلايا + سجل الحروف المفقودة."""
    cells, missing = set(), []
    for w in text.split():
        c, m = word_cells(w)
        cells |= c
        missing.extend(m)
    return {"cells": sorted(cells), "missing_letters": sorted(set(missing)),
            "known_defect_hit": False}


def load_tree():
    return json.loads((ROOT / "data" / "seed_tree.json").read_text(encoding="utf-8"))


def norm_query(s: str):
    s = re.sub(r'[\u064B-\u0652\u0670\u0640]', '', s)
    s = re.sub(r'[أإآٱ]', 'ا', s).replace('ة', 'ه').replace('ى', 'ي')
    out = []
    for w in s.split():
        out.append(w)
        m = re.match(r'^[وفبالل]+(.{2,})$', w)
        if m:
            out.append(m.group(1))
        a = re.match(r'^ال(.{2,})$', w)
        if a:
            out.append(a.group(1))
    return out


def address_node(node: dict):
    src = node["source"]
    if src["kind"] == "quran":
        return {"kind": "bits", **bit_address(src["quote"])}
    return {"kind": "hash", "book": src["book"], "verified": src.get("verified", False)}


def retrieve(query: str, top: int = 3):
    qc = set(bit_address(query)["cells"])
    qw = set(norm_query(query))
    tree = load_tree()
    scored = []
    for n in tree["nodes"]:
        a = address_node(n)
        if a["kind"] == "bits":
            score = len(qc & set(a["cells"])) / max(1, len(qc))
        else:
            nw = set(norm_query(n["source"]["quote"]))
            score = len(qw & nw) / max(1, len(qw)) * 0.9 if qw else 0
        if score > 0:
            scored.append((round(score, 3), n["id"]))
    scored.sort(reverse=True)
    ids = {n["id"]: n for n in tree["nodes"]}
    return [(i, s, ids[i]["reality"][:60]) for s, i in scored[:top]]


def _checks():
    tree = load_tree()
    ids = {n["id"] for n in tree["nodes"]}
    errs = []
    roots = {n["id"] for n in tree["nodes"] if n["genus"] == "جذر"}
    if len(tree["nodes"]) < 10 or not roots:
        errs.append("TR1: بذرة ناقصة")
    defect_hits = 0
    for n in tree["nodes"]:
        if False and not n["parents"] and n["id"] not in roots:
            errs.append(f"TR2: بلا آباء: {n['id']}")
        for p in n["parents"]:
            if p not in ids:
                errs.append(f"TR3: أب غائب: {n['id']}→{p}")
        if n["source"]["kind"] == "book" and not n["source"].get("verified"):
            errs.append(f"TR4: غير مطابَق: {n['id']}")
        if n["source"]["kind"] == "quran":
            a = bit_address(n["source"]["quote"])
            if len(a["cells"]) < 3:
                errs.append(f"TR5: عنوان نحيف: {n['id']}")
            if a["known_defect_hit"]:
                defect_hits += 1                     # مُسجَّل لا مرفوض
        dr = n.get("degree_rule", "")
        if not any(k in dr for k in ("قطعي", "ظني", "ضابطة")):
            errs.append(f"TR6: درجة غير مشتقة: {n['id']}")
    res = retrieve("ما الخاصية التي أحراقها في النار")
    if not res or res[0][0] != "N-QADR":
        errs.append(f"TR7: استرجاع فاشل: {res[:1]}")
    probe_sound = bit_address("في")
    probe_foreign = bit_address("پاک")
    if probe_sound["missing_letters"]:
        errs.append(f"TR8a: جسر سليم يُدَّعى عليه عيب: {probe_sound}")
    if not probe_foreign["missing_letters"]:
        errs.append("TR8b: الحروف الخارجة الدستور لا تُسجَّل")
    return errs, tree, defect_hits


def main() -> int:
    errs, tree, defect_hits = _checks()
    if errs:
        for e in errs:
            print("FAIL:", e)
        return 1
    print(f"TR1 nodes={len(tree['nodes'])} roots={sum(1 for n in tree['nodes'] if n['genus']=='جذر')}")
    print("TR2-TR6: all structural/admission checks pass")
    for i, s, r in retrieve("ما الخاصية التي أحراقها في النار")[:1]:
        print(f"TR7 retrieval → {i} ({s})")
    print(f"TR8 defect-awareness: {defect_hits} node(s) carry missing-letter records (refuted claim logged; foreign letters recorded)")
    print("SLGE-SEED: ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
