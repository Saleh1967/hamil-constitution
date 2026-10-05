#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prove_alama_hamila.py — قانون «العلامة حاملة والرتبة متبدلة».

يعيد اشتقاقَ برهان الإيداع 43 من الملف المقبوض في كل تشغيل:
H(حالة الخاتمة) + ثبات الخواتم + باب الخلو المشدود. لا يعمل بلا بصمة.
خرجُه مقفولٌ ببصمتَي الملف والأداة والوسائط."""
import hashlib, json, math, pathlib, re, sys, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORPUS = ROOT/"corpora"/"quran-simple-enhanced.txt"
DIAC = set("ًٌٍَُِّْٰـ")
AR = re.compile("[ء-غف-ي]")
def norm(t): return "".join(c for c in t if c not in DIAC)

def khana(t):
    chars = list(t); letters = [i for i,ch in enumerate(chars) if AR.match(ch)]
    if not letters: return None
    li = letters[-1]; last = chars[li]
    after = [ch for ch in chars[li+1:] if ch in DIAC]
    if last in "اى" and li-1 >= 0 and chars[li-1] == "ً": return "تنوين فتح"
    for tn, name in (("ً","تنوين فتح"),("ٌ","تنوين ضم"),("ٍ","تنوين كسر")):
        if tn in after: return name
    for hk, name in (("َ","فتحة"),("ُ","ضمة"),("ِ","كسرة"),("ْ","سكون")):
        if hk in after: return name
    if "ّ" in after: return "خلو مشدود"     # ← باب الخلو المُصنَّف: شدةٌ ظاهرة وسكونُها مقدَّر
    return "بلا علامة"

def main():
    if not CORPUS.exists(): sys.exit("لا مجمَّد في corpora/")
    data = CORPUS.read_bytes()
    tokens = [t for t in data.decode("utf-8").split() if AR.search(norm(t))]
    ks = [khana(t) for t in tokens]
    cnt = collections.Counter(ks); N = sum(cnt.values())
    H = -sum((c/N)*math.log2(c/N) for c in cnt.values())
    groups = collections.defaultdict(collections.Counter)
    for t,k in zip(tokens,ks): groups[norm(t)][k] += 1
    stable = {w for w,c in groups.items() if len(c)==1}
    occ = sum(sum(groups[w].values()) for w in stable)
    st2 = {w for w in stable if sum(groups[w].values())>=2}
    st2m = sum(sum(groups[w].values()) for w in st2)
    out = {"law": "ALAMA-HAMILA", "mazam": "الملف المقبوض وحده",
      "stable_v2_min2": {"types": len(st2), "mass": st2m, "mass_pct": round(st2m/N*100,1)},
           "H_khatma": round(H,4), "words": N, "khana_counts": dict(cnt.most_common()),
           "stable_types": len(stable), "bare_types": len(groups),
           "stable_mass": occ, "stable_mass_pct": round(occ/N*100,1),
           "_meta": {"corpus_sha256": hashlib.sha256(data).hexdigest(),
                     "tool_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                     "invocation": sys.argv}}
    (ROOT/"generated"/"alama_hamila_proof.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"H(الخاتمة)={H:.4f} | ثابتة: {len(stable)}/{len(groups)} ({occ/N*100:.1f}% من الكتلة) | خلو مشدود: {cnt['خلو مشدود']:,}")

if __name__ == "__main__":
    main()
