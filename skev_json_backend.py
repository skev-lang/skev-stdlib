"""
skev.json — Python Transpiler Backend
Copyright © 2026 AJ. All Rights Reserved. skev.dev
"""
import json as _json
from skev_runtime import succeed, fail

class JsonError:
    parse_failed  = "parse_failed"
    invalid_type  = "invalid_type"
    key_not_found = "key_not_found"
    encode_failed = "encode_failed"

def parse(json_str):
    try:
        result = _json.loads(str(json_str))
        # Return as JSON string for type-safe handling in Skev
        return succeed(_json.dumps(result))
    except (_json.JSONDecodeError, Exception):
        return fail(JsonError.parse_failed)

def stringify(value):
    try:
        if isinstance(value, str):
            # Try to parse as JSON first (if already JSON-encoded data)
            try:
                obj = _json.loads(value)
                return succeed(_json.dumps(obj, separators=(',', ':')))
            except:
                pass
        return succeed(_json.dumps(value, separators=(',', ':')))
    except Exception:
        return fail(JsonError.encode_failed)

def stringify_pretty(value, indent=2):
    try:
        if isinstance(value, str):
            try:
                obj = _json.loads(value)
                return succeed(_json.dumps(obj, indent=int(indent)))
            except:
                pass
        return succeed(_json.dumps(value, indent=int(indent)))
    except Exception:
        return fail(JsonError.encode_failed)

def is_valid(json_str):
    try:
        _json.loads(str(json_str))
        return True
    except:
        return False
