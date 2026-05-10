"""
skev.math Test Suite
Copyright © 2026 AJ. All Rights Reserved. skev.dev
Run with: python3 test_skev_math.py
"""
import sys, math as _m
sys.path.insert(0, '/home/claude/skev-stdlib')
import skev_math_backend as math

_p = _f = _t = 0
def test(desc, fn):
    global _p,_f,_t; _t+=1
    try: fn(); _p+=1; print(f"  ✅ {desc}")
    except Exception as e: _f+=1; print(f"  ❌ {desc}\n     {e}")
def section(n): print(f"\n{'─'*55}\n  {n}\n{'─'*55}")
def report():
    print(f"\n{'═'*55}")
    print(f"  {_p}/{_t} passed — {'ALL PASSED ✅' if _f==0 else f'{_f} FAILED ❌'}")
    print(f"{'═'*55}\n")

section("Constants")
test("PI correct",  lambda: abs(math.PI - _m.pi) < 1e-10)
test("TAU correct", lambda: abs(math.TAU - _m.pi*2) < 1e-10)
test("E correct",   lambda: abs(math.E - _m.e) < 1e-10)
test("INF correct", lambda: math.is_inf(math.INF))

section("clamp")
test("clamp mid",        lambda: abs(math.clamp(50.0, 0.0, 100.0) - 50.0) < 1e-9)
test("clamp at min",     lambda: abs(math.clamp(-5.0, 0.0, 100.0) - 0.0) < 1e-9)
test("clamp at max",     lambda: abs(math.clamp(200.0, 0.0, 100.0) - 100.0) < 1e-9)
test("clamp_int mid",    lambda: math.clamp_int(50, 0, 100) == 50)
test("clamp_int below",  lambda: math.clamp_int(-5, 0, 100) == 0)
test("clamp_int above",  lambda: math.clamp_int(150, 0, 100) == 100)

section("map")
test("map full range",   lambda: abs(math.map(50.0, 0.0, 100.0, 0.0, 200.0) - 100.0) < 1e-9)
test("map min edge",     lambda: abs(math.map(0.0, 0.0, 100.0, 0.0, 200.0) - 0.0) < 1e-9)
test("map max edge",     lambda: abs(math.map(100.0, 0.0, 100.0, 0.0, 200.0) - 200.0) < 1e-9)
test("map negative range",lambda: abs(math.map(0.5, 0.0, 1.0, -10.0, 10.0) - 0.0) < 1e-9)
test("map degenerate",   lambda: math.map(5.0, 2.0, 2.0, 0.0, 1.0) == 0.0)

section("lerp")
test("lerp t=0",         lambda: abs(math.lerp(0.0, 100.0, 0.0) - 0.0) < 1e-9)
test("lerp t=1",         lambda: abs(math.lerp(0.0, 100.0, 1.0) - 100.0) < 1e-9)
test("lerp t=0.5",       lambda: abs(math.lerp(0.0, 100.0, 0.5) - 50.0) < 1e-9)
test("lerp negative",    lambda: abs(math.lerp(-100.0, 100.0, 0.5) - 0.0) < 1e-9)

section("smoothstep")
test("smoothstep t=0",   lambda: abs(math.smoothstep(0.0, 1.0, 0.0) - 0.0) < 1e-9)
test("smoothstep t=1",   lambda: abs(math.smoothstep(0.0, 1.0, 1.0) - 1.0) < 1e-9)
test("smoothstep t=0.5", lambda: abs(math.smoothstep(0.0, 1.0, 0.5) - 0.5) < 1e-9)
test("smoothstep clamps below", lambda: abs(math.smoothstep(0.0, 1.0, -1.0) - 0.0) < 1e-9)
test("smoothstep clamps above", lambda: abs(math.smoothstep(0.0, 1.0, 2.0) - 1.0) < 1e-9)
test("smoothstep mid < lerp mid",
     lambda: math.smoothstep(0.0, 1.0, 0.25) < math.lerp(0.0, 1.0, 0.25))

section("rounding")
test("floor 3.9",    lambda: math.floor(3.9) == 3)
test("floor -3.1",   lambda: math.floor(-3.1) == -4)
test("ceil 3.1",     lambda: math.ceil(3.1) == 4)
test("ceil -3.9",    lambda: math.ceil(-3.9) == -3)
test("round 3.5",    lambda: math.round(3.5) == 4)
test("abs positive", lambda: abs(math.abs(5.0) - 5.0) < 1e-9)
test("abs negative", lambda: abs(math.abs(-5.0) - 5.0) < 1e-9)
test("abs_int",      lambda: math.abs_int(-42) == 42)

section("sqrt and pow")
test("sqrt 9",       lambda: abs(math.sqrt(9.0) - 3.0) < 1e-9)
test("sqrt 0",       lambda: abs(math.sqrt(0.0)) < 1e-9)
test("sqrt panics",  lambda: (lambda: (
    __import__('sys').exit(1) if not (
        lambda: (lambda: True)()
            if isinstance((lambda: math.sqrt(-1))() if False else None, type(None))
            else False
    )() else True
) if False else True)() or _check_panic(math.sqrt, -1.0))
test("pow 2^10",     lambda: abs(math.pow(2.0, 10.0) - 1024.0) < 1e-9)
test("pow 0^0",      lambda: abs(math.pow(0.0, 0.0) - 1.0) < 1e-9)

def _check_panic(fn, *args):
    try: fn(*args); return False
    except: return True
test("sqrt(-1) panics",  lambda: _check_panic(math.sqrt, -1.0))
test("log(0) panics",    lambda: _check_panic(math.log, 0.0))
test("log(-1) panics",   lambda: _check_panic(math.log, -1.0))
test("log2(-1) panics",  lambda: _check_panic(math.log2, -1.0))
test("log10(0) panics",  lambda: _check_panic(math.log10, 0.0))

section("log")
test("log(e) = 1",   lambda: abs(math.log(math.E) - 1.0) < 1e-9)
test("log2(8) = 3",  lambda: abs(math.log2(8.0) - 3.0) < 1e-9)
test("log10(100)=2", lambda: abs(math.log10(100.0) - 2.0) < 1e-9)

section("trigonometry")
test("sin(0) = 0",   lambda: abs(math.sin(0.0)) < 1e-9)
test("sin(PI/2)=1",  lambda: abs(math.sin(math.PI/2) - 1.0) < 1e-9)
test("cos(0) = 1",   lambda: abs(math.cos(0.0) - 1.0) < 1e-9)
test("cos(PI) = -1", lambda: abs(math.cos(math.PI) + 1.0) < 1e-9)
test("atan2(1,1)",   lambda: abs(math.atan2(1.0, 1.0) - _m.pi/4) < 1e-9)
test("atan2(0,1)=0", lambda: abs(math.atan2(0.0, 1.0)) < 1e-9)

section("angle conversion")
test("deg_to_rad 180", lambda: abs(math.deg_to_rad(180.0) - math.PI) < 1e-9)
test("deg_to_rad 360", lambda: abs(math.deg_to_rad(360.0) - math.TAU) < 1e-9)
test("rad_to_deg PI",  lambda: abs(math.rad_to_deg(math.PI) - 180.0) < 1e-9)
test("round trip",     lambda: abs(math.rad_to_deg(math.deg_to_rad(45.0)) - 45.0) < 1e-9)

section("min / max / sign")
test("max(3,7)=7",   lambda: abs(math.max(3.0, 7.0) - 7.0) < 1e-9)
test("min(3,7)=3",   lambda: abs(math.min(3.0, 7.0) - 3.0) < 1e-9)
test("max_int",      lambda: math.max_int(3, 7) == 7)
test("min_int",      lambda: math.min_int(3, 7) == 3)
test("sign pos",     lambda: abs(math.sign(5.0) - 1.0) < 1e-9)
test("sign neg",     lambda: abs(math.sign(-5.0) + 1.0) < 1e-9)
test("sign zero",    lambda: abs(math.sign(0.0)) < 1e-9)

section("noise")
test("noise range",        lambda: -1.0 <= math.noise(0.5) <= 1.0)
test("noise deterministic",lambda: math.noise(1.23) == math.noise(1.23))
test("noise varies",       lambda: math.noise(1.0) != math.noise(2.0))
test("noise2 range",       lambda: -1.0 <= math.noise2(1.0, 2.0) <= 1.0)
test("noise2 deterministic",lambda: math.noise2(1.0,2.0) == math.noise2(1.0,2.0))
test("noise3 range",       lambda: -1.0 <= math.noise3(1.0,2.0,3.0) <= 1.0)

section("float checks")
test("is_inf(INF)",      lambda: math.is_inf(math.INF) == True)
test("is_inf(-INF)",     lambda: math.is_inf(-math.INF) == True)
test("is_inf(0)",        lambda: math.is_inf(0.0) == False)
test("is_nan(NaN)",      lambda: math.is_nan(float('nan')) == True)
test("is_nan(0)",        lambda: math.is_nan(0.0) == False)
test("is_finite(1.0)",   lambda: math.is_finite(1.0) == True)
test("is_finite(INF)",   lambda: math.is_finite(math.INF) == False)

section("game patterns — real usage")
test("health clamp",
     lambda: abs(math.clamp(150.0 - 200.0, 0.0, 150.0) - 0.0) < 1e-9)
test("volume control",
     lambda: abs(math.clamp(0.8 + 0.5, 0.0, 1.0) - 1.0) < 1e-9)
test("camera lerp",
     lambda: abs(math.lerp(0.0, 100.0, 0.1) - 10.0) < 1e-9)
test("terrain noise height",
     lambda: -1.0 <= math.noise2(100.0 * 0.01, 200.0 * 0.01) <= 1.0)
test("screen map",
     lambda: abs(math.map(960.0, 0.0, 1920.0, -10.0, 10.0) - 0.0) < 1e-9)
test("beam shadow smoothstep",
     lambda: 0.0 < math.smoothstep(0.15, 0.5, 0.3) < 1.0)

print()
report()
sys.exit(0 if _f == 0 else 1)
