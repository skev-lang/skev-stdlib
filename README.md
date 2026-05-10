<!--
Copyright © 2026 AJ. All Rights Reserved.
Licensed under Apache 2.0. skev.dev | skev.org
-->

# Skev Standard Library

The Skev standard library — APIs and Python transpiler backends.

> These are the **Milestone 2.5** standard library APIs.
> The APIs are final and locked.
> The Python backends run today via the transpiler.
> Native implementations ship with Milestone 3 (real compiler).

---

## Modules

| Module | Status | Description |
|--------|--------|-------------|
| `skev.math` | ✅ Complete | Clamp, lerp, smoothstep, noise, trig |
| `skev.file` | ✅ Complete | Read, write, exists, list, paths |
| `skev.string` | ✅ Complete | Split, join, find, convert, pad |
| `skev.json` | ✅ Complete | Parse, stringify, validate |
| `skev.network` | ✅ API locked | HTTP GET/POST, url_encode |
| `skev.pkg` | ✅ Spec locked | Package manifest format |

---

## Quick Start

```bash
git clone https://github.com/skev-lang/skev-stdlib.git
cd skev-stdlib

# Run tests
python3 test_skev_math.py      # 82 tests
python3 test_skev_stdlib.py    # 67 tests (file + string + json)
```

---

## Test Results

```
skev.math          82/82  ✅
skev.file          67/67  ✅ (part of test_skev_stdlib.py)
skev.string        67/67  ✅ (part of test_skev_stdlib.py)
skev.json          67/67  ✅ (part of test_skev_stdlib.py)
```

---

## Usage (via transpiler)

```python
from skev_emitter import emit

source = """
import skev.math
import skev.file

entity Game >>
    score :: int = 0

    save_score() -> result[nothing]
        data :: string = "score:{score}"
        result file.write_text("save.txt", data)
    << save_score

<< Game
"""

code, errors = emit(source)
exec(code)
```

---

## Files

```
skev_math_api.skev         Public API definition
skev_math_backend.py       Python implementation
test_skev_math.py          82 tests

skev_file_api.skev         Public API definition
skev_file_backend.py       Python implementation

skev_string_api.skev       Public API definition
skev_string_backend.py     Python implementation

skev_json_api.skev         Public API definition
skev_json_backend.py       Python implementation

skev_network_api.skev      Public API definition
skev_network_backend.py    Python implementation

test_skev_stdlib.py        67 tests (file + string + json)

skev_pkg_spec.md           Package format specification
Skev_Cookbook.md           Common game patterns
```

---

## License

Apache License 2.0 — Copyright © 2026 AJ.

skev.dev | skev.org
