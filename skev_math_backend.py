"""
skev.math — Python Transpiler Backend
Copyright © 2026 AJ. All Rights Reserved. skev.dev

Implements the full skev.math API using Python's math module.
In the real Skev compiler these map to LLVM intrinsics.
Every function here is validated by test_skev_math.py.
"""

import math as _m
import hashlib as _h

# ── Constants ──────────────────────────────────────────────────
PI  = _m.pi
TAU = _m.pi * 2
E   = _m.e
INF = float('inf')

# ── Clamping and mapping ───────────────────────────────────────

def clamp(value, min_val, max_val):
    """Clamp value to [min_val, max_val]."""
    return max(float(min_val), min(float(max_val), float(value)))

def clamp_int(value, min_val, max_val):
    """Clamp integer to [min_val, max_val]."""
    return max(int(min_val), min(int(max_val), int(value)))

def map(value, in_min, in_max, out_min, out_max):
    """Map value from one range to another."""
    if in_max == in_min:
        return float(out_min)
    t = (float(value) - float(in_min)) / (float(in_max) - float(in_min))
    return float(out_min) + t * (float(out_max) - float(out_min))

# ── Interpolation ──────────────────────────────────────────────

def lerp(a, b, t):
    """Linear interpolation. t=0→a, t=1→b."""
    return float(a) + (float(b) - float(a)) * float(t)

def smoothstep(edge0, edge1, x):
    """Smooth interpolation with ease-in/ease-out."""
    t = clamp((float(x) - float(edge0)) / (float(edge1) - float(edge0)), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

# ── Rounding ───────────────────────────────────────────────────

def floor(x):    return int(_m.floor(float(x)))
def ceil(x):     return int(_m.ceil(float(x)))
def round(x):    return int(_m.floor(float(x) + 0.5))  # standard rounding
def abs(x):      return _m.fabs(float(x))
def abs_int(x):  return builtins_abs(int(x))

import builtins
builtins_abs = builtins.abs

# ── Power and roots ────────────────────────────────────────────

def sqrt(x):
    x = float(x)
    if x < 0:
        raise RuntimeError(f"[SKEV PANIC] math.sqrt received negative: {x}")
    return _m.sqrt(x)

def pow(base, exp):  return _m.pow(float(base), float(exp))

def log(x):
    x = float(x)
    if x <= 0:
        raise RuntimeError(f"[SKEV PANIC] math.log received non-positive: {x}")
    return _m.log(x)

def log2(x):
    x = float(x)
    if x <= 0:
        raise RuntimeError(f"[SKEV PANIC] math.log2 received non-positive: {x}")
    return _m.log2(x)

def log10(x):
    x = float(x)
    if x <= 0:
        raise RuntimeError(f"[SKEV PANIC] math.log10 received non-positive: {x}")
    return _m.log10(x)

# ── Trigonometry ───────────────────────────────────────────────

def sin(x):       return _m.sin(float(x))
def cos(x):       return _m.cos(float(x))
def tan(x):       return _m.tan(float(x))
def atan2(y, x):  return _m.atan2(float(y), float(x))
def asin(x):      return _m.asin(float(x))
def acos(x):      return _m.acos(float(x))

# ── Angle conversion ───────────────────────────────────────────

def deg_to_rad(d): return float(d) * (_m.pi / 180.0)
def rad_to_deg(r): return float(r) * (180.0 / _m.pi)

# ── Min / Max / Sign ───────────────────────────────────────────

def max(a, b):     return float(a) if float(a) > float(b) else float(b)
def min(a, b):     return float(a) if float(a) < float(b) else float(b)
def max_int(a, b): return int(a) if int(a) > int(b) else int(b)
def min_int(a, b): return int(a) if int(a) < int(b) else int(b)

def sign(x):
    x = float(x)
    if x > 0: return  1.0
    if x < 0: return -1.0
    return 0.0

# ── Noise ──────────────────────────────────────────────────────

def _hash_noise(*coords):
    key = ",".join(f"{c:.4f}" for c in coords)
    h = int(_h.md5(key.encode()).hexdigest()[:8], 16)
    return (h / 0xFFFFFFFF) * 2.0 - 1.0  # -1.0 to 1.0

def noise(x):          return _hash_noise(float(x))
def noise2(x, y):      return _hash_noise(float(x), float(y))
def noise3(x, y, z):   return _hash_noise(float(x), float(y), float(z))

# ── Float checks ───────────────────────────────────────────────

def is_inf(x):    return _m.isinf(float(x))
def is_nan(x):    return _m.isnan(float(x))
def is_finite(x): return _m.isfinite(float(x))
