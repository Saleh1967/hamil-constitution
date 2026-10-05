import json, pathlib, subprocess, sys, csv
ROOT = pathlib.Path(__file__).resolve().parent.parent
def test_carrier_law():
    r = subprocess.run([sys.executable, str(ROOT/"tools/prove_alama_hamila.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-300:]
    assert "خلو مشدود: 0" in r.stdout
def test_fingerprints_match():
    fe = json.loads((ROOT/"data/fingerprints.expected.json").read_text(encoding="utf-8"))
    fa = json.loads((ROOT/"data/fingerprints.json").read_text(encoding="utf-8"))
    for k, v in (fe.get("files", fe)).items():
        assert fa[k]["git_sha"] == v["git_sha"], k
def test_roots_in_alphabet():
    alpha = set("ءابتثجحخدذرزسشصضطظعغفقكلمنهوي")
    with open(ROOT/"data/verb_triliteral.csv", encoding="utf-8") as f:
        rd = csv.reader(f, delimiter="	"); next(rd)
        for row in rd:
            if len(row) >= 5:
                assert all(ch in alpha for ch in row[1].replace("أ","ء")), row[1]
