"""
skev.string — Python Transpiler Backend
Copyright © 2026 AJ. All Rights Reserved. skev.dev
"""
from skev_runtime import some, nothing

def length(s):              return len(str(s))
def contains(s, substr):    return str(substr) in str(s)
def starts_with(s, prefix): return str(s).startswith(str(prefix))
def ends_with(s, suffix):   return str(s).endswith(str(suffix))
def trim(s):                return str(s).strip()
def upper(s):               return str(s).upper()
def lower(s):               return str(s).lower()
def replace(s, old, new_s): return str(s).replace(str(old), str(new_s))
def split(s, sep):          return str(s).split(str(sep))
def join(parts, sep):       return str(sep).join(str(p) for p in parts)
def repeat(s, n):           return str(s) * max(0, int(n))
def is_blank(s):            return len(str(s).strip()) == 0

def substr(s, start, length):
    s = str(s); start = int(start); length = int(length)
    if start < 0 or start >= len(s) or length <= 0:
        return nothing()
    result = s[start:start+length]
    return some(result) if result else nothing()

def find(s, substr):
    idx = str(s).find(str(substr))
    return some(idx) if idx >= 0 else nothing()

def pad_left(s, width, pad_char):
    return str(s).rjust(int(width), str(pad_char)[0] if pad_char else ' ')

def pad_right(s, width, pad_char):
    return str(s).ljust(int(width), str(pad_char)[0] if pad_char else ' ')

def from_int(n):                    return str(int(n))
def from_float(x, decimal_places):  return f"{float(x):.{int(decimal_places)}f}"

def to_int(s):
    try:    return some(int(str(s).strip()))
    except: return nothing()

def to_float(s):
    try:    return some(float(str(s).strip()))
    except: return nothing()
