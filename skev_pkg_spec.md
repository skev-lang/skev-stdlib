<!--
Copyright © 2026 AJ. All Rights Reserved.
skev.dev | skev.org
-->

# skev.pkg — Package Format Specification
**Version:** 1.0 | **Status:** Locked

---

## Package Manifest: `skev.pkg`

Every Skev package has one `skev.pkg` file at its root.

```
name:     "my-game"
version:  "1.0.0"
author:   "AJ"
license:  "MIT"

dependencies >>
    skev.math:    ">=1.0.0"
    skev.network: ">=2.0.0"
    physics-lib:  "1.4.2"
<< dependencies

capabilities >>
    file.read
    file.write
    network.outbound
<< capabilities

targets >>
    ios
    android
    macos
    windows
    linux
<< targets
```

---

## Directory Structure

```
my-package/
  skev.pkg          ← manifest (required)
  src/
    main.skev       ← entry point
    lib/
      player.skev
      enemy.skev
  tests/
    test_player.skev
  assets/
    sounds/
    textures/
  README.md
```

---

## Version Format

Semantic versioning: `MAJOR.MINOR.PATCH`

```
"1.0.0"    exact version
">=1.0.0"  minimum version
"^1.2.0"   compatible (same major)
"~1.2.0"   patch updates only
"*"        any version
```

---

## CLI Commands

```bash
skev init my-package          # create new package
skev build                    # compile current package
skev test                     # run test suite
skev run                      # build and run
skev install physics-lib      # add dependency
skev add physics-lib@1.4.2    # add specific version
skev remove physics-lib       # remove dependency
skev publish                  # publish to registry
skev publish --github         # publish via GitHub
```

---

## GitHub Distribution (Primary)

Before an official registry exists, packages are distributed via GitHub:

```
# Install from GitHub:
skev install github.com/skev-lang/physics-lib

# Install specific version (git tag):
skev install github.com/skev-lang/physics-lib@v1.4.2

# skev.pkg reference:
dependencies >>
    physics-lib: "github.com/skev-lang/physics-lib@1.4.2"
<< dependencies
```

---

## Capabilities

Packages must declare what system access they need.
The sandbox (Chapter 10) enforces these at runtime.

```
file.read           read files in allowed paths
file.write          write files in allowed paths
network.outbound    make outgoing network connections
network.server      listen for incoming connections
process.spawn       start child processes
gpu.compute         use GPU compute shaders
```

Undeclared capability access = compile error.

---

*Copyright © 2026 AJ. All Rights Reserved. skev.dev | skev.org*
