import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
ALPHA = set("ءابتثجحخدذرزسشصضطظعغفقكلمنهوي")

def _norm(r):
    for a, b in (("أ","ء"),("إ","ء"),("آ","ء"),("ؤ","ء"),("ئ","ء"),("ى","ا")):
        r = r.replace(a, b)
    return r

def test_source_seat_convention_declared():
    """دَين المصدر معلن: ابن فارس يكتب الجذور بمقاعد غير مطبعة (322 أ، 145 ى) — طبعنا له أثبت عدم الوراثة العمياء"""
    rows = list(csv.DictReader(open(ROOT/"data/maqayis_by_root_csv_999.csv", encoding="utf-8")))
    raw_bad = sum(1 for r in rows if any(c not in ALPHA for c in r["root_full"]))
    assert raw_bad > 0                       # الدين موجود في المصدر كما هو
    assert all(all(c in ALPHA for c in _norm(r["root_full"])) for r in rows)  # ويزول بطبعنا

def test_quadriliterals_named():
    rows = list(csv.DictReader(open(ROOT/"data/maqayis_by_root_csv_999.csv", encoding="utf-8")))
    quad = sorted({_norm(r["root_full"]) for r in rows if len(_norm(r["root_full"])) == 4})
    assert quad == ["ثءثء", "جءجء", "جهجه"]   # ثلاثة ثوابع، كلها معلنة بالاسم (بترتيب الفرز)
