<!--
Copyright © 2026 AJ. All Rights Reserved. skev.dev | skev.org
-->

# Skev Community Setup Guide
**Version:** 1.0

---

## GitHub Organisation: `skev-lang`

### Repositories to Create

```
github.com/skev-lang/

  skev             ← compiler (Milestone 3, main repo)
  skev-spec        ← specification documents
  skev-transpiler  ← Python transpiler (417 tests)
  skev-vscode      ← VS Code extension
  skev-examples    ← cookbook programs
  skev-stdlib      ← standard library (post M3)
  skev-www         ← skev.dev website
```

### Repository Setup for `skev` (main)

```
README.md          ← what Skev is, install, quickstart
CONTRIBUTING.md    ← how to contribute
LICENSE            ← Apache 2.0
CHANGELOG.md       ← version history
CODE_OF_CONDUCT.md ← community standards
.github/
  ISSUE_TEMPLATE/
    bug_report.md
    feature_request.md
  PULL_REQUEST_TEMPLATE.md
```

### Labels for Issues

```
Type:
  bug           red
  enhancement   blue
  question      yellow
  discussion    purple

Area:
  compiler      orange
  stdlib        green
  tooling       teal
  docs          grey
  spec          lavender

Priority:
  critical      bright red
  high          orange
  medium        yellow
  low           grey
```

---

## Discord Server: Skev

### Channels

```
WELCOME
  #welcome          rules, links, intro
  #announcements    milestone updates, releases
  #introduce-yourself

LANGUAGE
  #general          general Skev discussion
  #spec-questions   questions about the spec
  #show-and-tell    share Skev code

DEVELOPMENT
  #compiler         M3 compiler work
  #stdlib           standard library
  #tooling          IDE, grammar, editor support

COMMUNITY
  #off-topic        anything else
  #feedback         suggestions for Skev
```

---

## Social Presence

```
GitHub:   github.com/skev-lang        ← primary
Twitter:  @skev_lang                  ← announcements
Mastodon: @skev@fosstodon.org         ← community
Reddit:   r/skev_lang                 ← discussions
```

### Announcement Template

```
🎯 Skev Milestone 3 — Real Compiler Ships

The Skev compiler (Rust + LLVM) passes all 417 compliance tests.
.skev files now compile to native code on macOS, Linux, Windows.

→ github.com/skev-lang/skev
→ skev.dev

#gamedevelopment #programming #gamedev
```

---

*Copyright © 2026 AJ. All Rights Reserved. skev.dev | skev.org*
