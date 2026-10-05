#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""منفّذ الاختبارات بفصل سريع/ثقيل: python3 tools/run_tests.py [--all]"""
import importlib.util, inspect, pathlib, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
FAST = {"test_slge.py", "test_tree.py", "test_carrier.py"}
sys.path.insert(0, str(ROOT / "src" / "slge"))


def main():
    all_mode = "--all" in sys.argv
    files = sorted((ROOT / "tests").glob("test_*.py"))
    if not all_mode:
        files = [f for f in files if f.name in FAST]
    sys.modules['pytest'] = type(sys)('pytest')  # stub
    passed = failed = 0
    for f in files:
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception:
            failed += 1
            continue
        for name in sorted(dir(mod)):
            if name.startswith('test_'):
                fn = getattr(mod, name)
                try:
                    if 'tmp_path' in inspect.signature(fn).parameters:
                        fn(pathlib.Path(tempfile.mkdtemp()))
                    else:
                        fn()
                    passed += 1
                except Exception:
                    failed += 1
                    print('FAIL', f.name, name)
    print(f'{"ALL" if all_mode else "FAST"}: {passed} passed / {failed} failed')
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
