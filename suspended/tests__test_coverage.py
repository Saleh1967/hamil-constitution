import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"src/slge"))
import slge, slge_laws

def test_legacy_deep_claims_declared_absent():
    # deep_claims.py غير موجود في أي مصدر مودع (burhan zip ولا Taaqol-GPT) — غيابٌ معلنٌ موثق
    assert not (ROOT/"legacy/deep_claims.py").exists()
    assert "deep_claims" in (ROOT/"docs/COVERAGE_MATRIX.md").read_text(encoding="utf-8")

def test_legacy_seg_context():
    assert slge_laws.to_atoms("بِسْمِ")[0][1] != "سكون"
    for word in ["ٱلرَّحِيمِ", "ٱلْحَمْدُ", "ٱللَّهِ"]:
        assert slge_laws.begin(slge_laws.to_atoms(word))[0][1] != "سكون", word
