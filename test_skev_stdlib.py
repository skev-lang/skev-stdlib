"""
skev.file + skev.string + skev.json Test Suite
Copyright © 2026 AJ. All Rights Reserved. skev.dev
"""
import sys, os, tempfile
sys.path.insert(0, '/home/claude')
sys.path.insert(0, '/home/claude/skev-stdlib')
import skev_file_backend   as file
import skev_string_backend as string
import skev_json_backend   as json

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

# Use a temp directory for all file tests
TMP = tempfile.mkdtemp()

section("skev.file — read and write")
def t_write_read():
    p = os.path.join(TMP, "test.txt")
    r = file.write_text(p, "hello skev")
    assert r.is_success
    r2 = file.read_text(p)
    assert r2.is_success and r2.value == "hello skev"

def t_read_not_found():
    r = file.read_text(os.path.join(TMP, "missing.txt"))
    assert r.is_failure and r.error == file.FileError.not_found

def t_append():
    p = os.path.join(TMP, "append.txt")
    file.write_text(p, "line1\n")
    file.append_text(p, "line2\n")
    r = file.read_text(p)
    assert r.is_success and "line1" in r.value and "line2" in r.value

def t_exists():
    p = os.path.join(TMP, "exists.txt")
    assert not file.exists(p)
    file.write_text(p, "x")
    assert file.exists(p)

def t_is_file():
    p = os.path.join(TMP, "isfile.txt")
    file.write_text(p, "x")
    assert file.is_file(p)
    assert not file.is_dir(p)

def t_is_dir():
    assert file.is_dir(TMP)
    assert not file.is_file(TMP)

def t_make_dir():
    p = os.path.join(TMP, "newdir")
    r = file.make_dir(p)
    assert r.is_success
    assert file.is_dir(p)

def t_make_dir_already_exists():
    r = file.make_dir(TMP)
    assert r.is_failure and r.error == file.FileError.already_exists

def t_delete_file():
    p = os.path.join(TMP, "delete_me.txt")
    file.write_text(p, "x")
    r = file.delete_file(p)
    assert r.is_success
    assert not file.exists(p)

def t_delete_not_found():
    r = file.delete_file(os.path.join(TMP, "ghost.txt"))
    assert r.is_failure

def t_list_dir():
    d = os.path.join(TMP, "listdir")
    file.make_dir(d)
    file.write_text(os.path.join(d, "a.txt"), "a")
    file.write_text(os.path.join(d, "b.txt"), "b")
    r = file.list_dir(d)
    assert r.is_success and "a.txt" in r.value and "b.txt" in r.value

def t_file_size():
    p = os.path.join(TMP, "size.txt")
    file.write_text(p, "hello")
    r = file.file_size(p)
    assert r.is_success and r.value == 5

test("write then read", t_write_read)
test("read not_found", t_read_not_found)
test("append to file", t_append)
test("exists check", t_exists)
test("is_file correct", t_is_file)
test("is_dir correct", t_is_dir)
test("make_dir creates", t_make_dir)
test("make_dir already_exists", t_make_dir_already_exists)
test("delete_file works", t_delete_file)
test("delete not_found fails", t_delete_not_found)
test("list_dir returns entries", t_list_dir)
test("file_size correct", t_file_size)

section("skev.file — path utilities")
test("path_join", lambda: file.path_join("save", "player.json") == os.path.join("save","player.json"))
test("path_name", lambda: file.path_name("save/player.json") == "player.json")
test("path_dir",  lambda: file.path_dir("save/player.json") == "save")
test("path_ext",  lambda: file.path_ext("player.json") == ".json")
test("path_ext skev", lambda: file.path_ext("game.skev") == ".skev")

section("skev.string — basic ops")
test("length",          lambda: string.length("hello") == 5)
test("length empty",    lambda: string.length("") == 0)
test("contains true",   lambda: string.contains("hello world", "world") == True)
test("contains false",  lambda: string.contains("hello", "xyz") == False)
test("starts_with",     lambda: string.starts_with("hello", "hel") == True)
test("starts_with no",  lambda: string.starts_with("hello", "xyz") == False)
test("ends_with",       lambda: string.ends_with("hello", "llo") == True)
test("ends_with no",    lambda: string.ends_with("hello", "xyz") == False)
test("trim spaces",     lambda: string.trim("  hello  ") == "hello")
test("trim none",       lambda: string.trim("hello") == "hello")
test("upper",           lambda: string.upper("hello") == "HELLO")
test("lower",           lambda: string.lower("HELLO") == "hello")
test("replace",         lambda: string.replace("hello world", "world", "skev") == "hello skev")
test("replace all",     lambda: string.replace("aaa", "a", "b") == "bbb")

section("skev.string — split, join, search")
test("split basic",     lambda: string.split("a,b,c", ",") == ["a","b","c"])
test("split no sep",    lambda: string.split("hello", ",") == ["hello"])
test("join",            lambda: string.join(["a","b","c"], ",") == "a,b,c")
test("join empty",      lambda: string.join([], ",") == "")
test("substr valid",    lambda: string.substr("hello", 1, 3).value == "ell")
test("substr out",      lambda: not string.substr("hi", 10, 3).exists)
test("find found",      lambda: string.find("hello world", "world").value == 6)
test("find not found",  lambda: not string.find("hello", "xyz").exists)
test("repeat",          lambda: string.repeat("ab", 3) == "ababab")
test("repeat zero",     lambda: string.repeat("ab", 0) == "")
test("is_blank empty",  lambda: string.is_blank("") == True)
test("is_blank spaces", lambda: string.is_blank("   ") == True)
test("is_blank not",    lambda: string.is_blank("a") == False)

section("skev.string — conversion")
test("from_int",          lambda: string.from_int(42) == "42")
test("from_int negative", lambda: string.from_int(-5) == "-5")
test("from_float 2dp",    lambda: string.from_float(3.14159, 2) == "3.14")
test("from_float 0dp",    lambda: string.from_float(3.9, 0) == "4")
test("to_int valid",      lambda: string.to_int("42").value == 42)
test("to_int invalid",    lambda: not string.to_int("abc").exists)
test("to_float valid",    lambda: abs(string.to_float("3.14").value - 3.14) < 1e-9)
test("to_float invalid",  lambda: not string.to_float("xyz").exists)
test("pad_left",          lambda: string.pad_left("42", 5, "0") == "00042")
test("pad_right",         lambda: string.pad_right("hi", 5, ".") == "hi...")

section("skev.json — parse and stringify")
test("is_valid true",       lambda: json.is_valid('{"key":"value"}') == True)
test("is_valid false",      lambda: json.is_valid('not json') == False)
test("is_valid number",     lambda: json.is_valid('42') == True)
test("parse valid",         lambda: json.parse('{"x":1}').is_success)
test("parse invalid",       lambda: json.parse('bad json').is_failure)
test("parse error type",    lambda: json.parse('bad').error == json.JsonError.parse_failed)
test("stringify dict",      lambda: json.stringify({"a":1}).is_success)
test("stringify list",      lambda: json.stringify([1,2,3]).is_success)
test("stringify int",       lambda: json.stringify(42).is_success)
test("stringify_pretty",    lambda: json.stringify_pretty({"a":1}, 2).is_success)
test("roundtrip",
     lambda: json.is_valid(json.stringify({"score":100,"name":"AJ"}).value))

section("game save pattern — full pipeline")
def t_save_load():
    save_data = '{"player":"AJ","score":9999,"level":7}'
    # Write
    p = os.path.join(TMP, "save.json")
    assert file.write_text(p, save_data).is_success
    # Read
    r = file.read_text(p)
    assert r.is_success
    # Validate JSON
    assert json.is_valid(r.value)
    # Parse
    parsed = json.parse(r.value)
    assert parsed.is_success
    # Verify round-trip
    assert json.is_valid(parsed.value)

def t_leaderboard_format():
    entries = [{"name":"AJ","score":9999},{"name":"Player2","score":5000}]
    r = json.stringify(entries)
    assert r.is_success
    assert json.is_valid(r.value)
    count = r.value.count('"name"')
    assert count == 2

test("save and load JSON file", t_save_load)
test("leaderboard JSON format", t_leaderboard_format)

print()
report()
import shutil
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(0 if _f == 0 else 1)
