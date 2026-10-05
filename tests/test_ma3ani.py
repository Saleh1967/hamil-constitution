# -*- coding: utf-8 -*-
"""Tests for SLGE-MA3ANI — دلالات المعاني النحوية (معاني النحو، السامرائّي)."""
import importlib.util, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("slge_ma3ani", ROOT / "src" / "slge" / "slge_ma3ani.py")
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)


def test_ma1_core_meanings_present():
    assert ma.MA1_CORE_MEANING["الباء"]["أصل"] == "الإلصاق"
    assert ma.MA1_CORE_MEANING["على"]["أصل"] == "الاستعلاء"
    assert ma.MA1_CORE_MEANING["من"]["أصل"] == "الابتداء"
    assert ma.MA1_CORE_MEANING["عن"]["أصل"] == "المجاوزة (الابتعاد)"
    assert ma.MA1_CORE_MEANING["حتى"]["أصل"].startswith("غاية الاستئصال")
    assert ma.MA1_CORE_MEANING["اللام"]["أصل"] == "الاختصاص"


def test_ma2_no_symmetric_substitution():
    # اللام والباء يحملان التعليل لكن بغير وصف
    descs = list(ma.MA2_SHARED_MEANING["التعليل"].values())
    assert len(set(descs)) == len(descs)


def test_ma3_tadmim_three_conditions():
    assert len(ma.MA3_TADMIM["الشروط"]) == 3
    assert any("الرفث" in s["نص"] for s in ma.MA3_TADMIM["شواهد"])


def test_ma4_verb_distinctions():
    d = ma.MA4_DISTINCTIONS["علم_vs_عرف"]
    assert "الصفات" in d["علم"] and "الذوات" in d["عرف"]
    r = ma.MA4_DISTINCTIONS["أفعال_الرجحان"]
    assert all(k in r for k in ("ظن", "حسب", "خال", "زعم"))


def test_ma6_two_kinds_of_absence():
    assert "لدليل" in ma.MA6_HADF["الضرب_الأول_اختصار"]["تعريف"]
    assert "القاصر" in ma.MA6_HADF["الضرب_الثاني_اقتصار"]["تعريف"]


def test_ma7_iyyaka_substitution():
    assert "نائبة" in ma.MA7_TAHDHIR["بنية_إياك"]
    assert "هياك" in ma.MA7_TAHDHIR["التفرقة"]


def test_ma8_good_named_evil_passive():
    assert ma.MA8_NAIB["شواهد_الخير_الظاهر"] and ma.MA8_NAIB["شواهد_الشر_المجهول"]


def test_main_exits_zero():
    assert ma.main() == 0
