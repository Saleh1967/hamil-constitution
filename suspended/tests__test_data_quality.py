# -*- coding: utf-8 -*-
"""فحص جودة البيانات على المخطط — العيوب المعلنة تُفحص لا تُخفى."""
import csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_maqayis_schema_and_known_defects():
    rows = list(csv.DictReader(open(ROOT / "data/maqayis_by_root_csv_999.csv", encoding="utf-8-sig")))
    assert len(rows) == 4576, "عدد المواد انزاح"
    cols = set(rows[0].keys())
    assert "root_full" in cols, "عمود الجذر غائب"
    axes = "semantic_axes"
    assert axes in cols, "عمود المحاور الدلالية غائب من المخطط"
    empty = sum(1 for r in rows if not (r.get(axes) or "").strip())
    assert empty == 1632, "عيب معلن انزاح: فراغ المحاور لم يعد كما في البطاقة"
