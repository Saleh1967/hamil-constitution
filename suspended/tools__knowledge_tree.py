#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
واجهة سطر أوامر لشجرة المعرفة — غلاف رفيع فوق محرك SLGE-SEED
(src/slge/slge_seed.py). المنطق الكامل (العنوان البتّي، الاسترجاع، الثوابت) في المحرك.
"""
import importlib.util, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("slge_seed", ROOT / "src" / "slge" / "slge_seed.py")
tr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tr)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        return tr.main()
    q = sys.argv[1] if len(sys.argv) > 1 else "ما الخاصية التي في النار"
    for i, s, r in tr.retrieve(q):
        print(f"{s:.2f}  {i}  {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
