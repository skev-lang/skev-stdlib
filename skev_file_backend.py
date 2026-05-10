"""
skev.file — Python Transpiler Backend
Copyright © 2026 AJ. All Rights Reserved. skev.dev
"""
import os as _os, pathlib as _p

class FileError:
    not_found         = "not_found"
    permission_denied = "permission_denied"
    already_exists    = "already_exists"
    is_directory      = "is_directory"
    disk_full         = "disk_full"
    invalid_path      = "invalid_path"
    read_error        = "read_error"
    write_error       = "write_error"

def _ok(v=None):
    from skev_runtime import succeed
    return succeed(v)

def _err(e):
    from skev_runtime import fail
    return fail(e)

def read_text(path):
    try:
        with open(str(path), 'r', encoding='utf-8') as f:
            return _ok(f.read())
    except FileNotFoundError: return _err(FileError.not_found)
    except PermissionError:   return _err(FileError.permission_denied)
    except IsADirectoryError: return _err(FileError.is_directory)
    except Exception:         return _err(FileError.read_error)

def write_text(path, content):
    try:
        _p.Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(str(path), 'w', encoding='utf-8') as f:
            f.write(str(content))
        return _ok()
    except PermissionError: return _err(FileError.permission_denied)
    except OSError:         return _err(FileError.write_error)

def append_text(path, content):
    try:
        with open(str(path), 'a', encoding='utf-8') as f:
            f.write(str(content))
        return _ok()
    except PermissionError: return _err(FileError.permission_denied)
    except Exception:       return _err(FileError.write_error)

def exists(path):     return _os.path.exists(str(path))
def is_file(path):    return _os.path.isfile(str(path))
def is_dir(path):     return _os.path.isdir(str(path))

def make_dir(path):
    try:
        _os.mkdir(str(path))
        return _ok()
    except FileExistsError:  return _err(FileError.already_exists)
    except PermissionError:  return _err(FileError.permission_denied)

def make_dir_all(path):
    try:
        _p.Path(path).mkdir(parents=True, exist_ok=True)
        return _ok()
    except PermissionError: return _err(FileError.permission_denied)

def delete_file(path):
    try:
        _os.remove(str(path))
        return _ok()
    except FileNotFoundError: return _err(FileError.not_found)
    except PermissionError:   return _err(FileError.permission_denied)
    except IsADirectoryError: return _err(FileError.is_directory)

def list_dir(path):
    try:
        entries = sorted(_os.listdir(str(path)))
        return _ok(entries)
    except FileNotFoundError: return _err(FileError.not_found)
    except NotADirectoryError: return _err(FileError.is_directory)
    except PermissionError:   return _err(FileError.permission_denied)

def file_size(path):
    try:
        return _ok(_os.path.getsize(str(path)))
    except FileNotFoundError: return _err(FileError.not_found)

def path_join(a, b):  return str(_p.Path(str(a)) / str(b))
def path_name(path):  return _p.Path(str(path)).name
def path_dir(path):   return str(_p.Path(str(path)).parent)
def path_ext(path):   return _p.Path(str(path)).suffix
