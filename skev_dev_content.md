<!--
Copyright © 2026 AJ. All Rights Reserved. skev.dev | skev.org
-->

# skev.dev — Website Content
**Version:** 1.0 | Content for all pages

---

## Landing Page (/)

**Headline:**
```
Skev
Fast like C++. Easy to read like Python.
Built for games, XR, and real-time systems.
```

**Tagline:**
```
The language that speaks games natively.
Vector3! is a primitive. entity is a keyword.
No GC pauses. No null crashes. No boilerplate.
```

**Code sample (hero):**
```swift
entity Player >>
    position :: Vector3!
    health   :: int = 100
    alive    :: bool = true

    has Physics

    when collision(other: Enemy)
        health -|= other.damage
        if health <= 0 >>
            alive = false
        << health <= 0
    << collision: Enemy

<< Player
```

**Three pillars:**
```
GAME-NATIVE          SAFE BY DEFAULT      READABLE AT SCALE
Vector3! Color!      ARC memory           >> << block labels
Transform! Quat!     maybe T              Every block named
Built-in entity      result[T]            Never lost at line 500
Built-in events      No null crashes      No brace counting
```

**CTA:**
```
[Read the Spec]   [View on GitHub]   [Follow Progress]
```

---

## Why Skev (/why)

```
C++ is the industry standard for games.
It is also 30+ years of technical debt,
undefined behaviour, and build system chaos.

C# and Unity are excellent.
The GC pauses are real. Frame spikes happen.
Every Unity developer has lost an hour to garbage collection.

Rust is memory-safe without GC.
The borrow checker is correct.
It also fights you every time you try to mutate
an entity that two systems need to access.

Skev makes different trade-offs:

  ARC memory — no GC, no manual free, no borrow checker
  Game-native types — Vector3! is a language primitive
  Built-in entity system — entity and when are keywords
  result[T] enforcement — ignoring errors is a compile error
  maybe T — null pointer crashes are impossible

Skev is not trying to be everything.
It is trying to be the best language for games,
XR, simulations, and real-time systems.
Nothing else.
```

---

## Roadmap (/roadmap)

```
MILESTONE 1   ✅ COMPLETE
Specification
  11 chapters + 3.5
  All design decisions locked
  Apache 2.0 licensed

MILESTONE 2   ✅ COMPLETE
Python Transpiler
  417 tests passing
  8 complete programs running
  Full pipeline: .skev → Python → exec()

MILESTONE 2.5  ✅ COMPLETE
Pre-Compiler Work
  TextMate grammar
  VS Code extension
  Standard library APIs
  SOA, overflow, data race specs

MILESTONE 3   ⬜ IN PROGRESS
Real Compiler
  Rust + LLVM backend
  417 tests = compliance suite
  macOS, Linux, Windows, iOS, Android

MILESTONE 4   ⬜ PLANNED
Standard Library + First Game
  skev.math  skev.file  skev.string
  skev.json  skev.network  skev.render
  Road Fighter-inspired mobile game (shipped)

MILESTONE 5   ⬜ PLANNED
Skev Studio
  IDE built in Skev
  LSP, debugger, hot reload

MILESTONE 6   ⬜ FUTURE
Self-Hosting
  Skev compiler written in Skev
  The maturity milestone
```

---

## Spec (/spec)

```
The complete Skev language specification.
All 11 chapters are open and free.

Chapter 1:  Introduction & Philosophy
Chapter 2:  Syntax & Structure
Chapter 3:  Data Types (+ SOA 3.11, Overflow 3.12)
Chapter 3.5: Generics
Chapter 4:  Memory Model (ARC)
Chapter 5:  Concurrency (+ Data Race 5.8)
Chapter 6:  Error Handling
Chapter 7:  Standard Library
Chapter 8:  Interoperability (FFI)
Chapter 9:  Build System
Chapter 10: Safety & Sandboxing
Chapter 11: Tooling

Copyright © 2026 AJ. All Rights Reserved.
Apache 2.0 for compiler, spec, and standard library.
```

---

*Copyright © 2026 AJ. All Rights Reserved. skev.dev | skev.org*
