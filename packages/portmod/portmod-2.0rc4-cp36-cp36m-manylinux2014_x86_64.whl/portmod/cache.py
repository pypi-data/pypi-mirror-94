# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""Module for handling the pybuild cache"""

import json
import os
from typing import Dict, cast

from .atom import FQAtom
from .config import get_config
from .fs.util import get_hash
from .globals import env, get_version
from .perms import Permissions
from .pybuild import FullInstalledPybuild, FullPybuild, InstalledPybuild, Pybuild
from .repo import get_repo
from .repo.loader import get_atom_from_path
from .repo.metadata import get_masters


class PreviouslyEncounteredException(Exception):
    """Exception that has previously occurred and should be ignored"""

    def __init__(self, previous: Exception):
        super().__init__()
        self.previous = previous


# We store a cache of mods so that they are only loaded once
# when doing dependency resolution.
# Stores key-value pairs of the form (filename, Mod Object)
class Cache:
    _mods: Dict[str, Pybuild] = {}
    _failed: Dict[str, Exception] = {}

    def __init__(self):
        self._mods = {}

    def clear(self):
        self._mods = {}
        self._failed = {}

    def clear_path(self, path: str):
        if path in self._mods:
            del self._mods[path]
        if path in self._failed:
            del self._failed[path]


cache = Cache()


def clear_cache_for_path(path: str):
    """
    Clears the mod cache for the given path

    Should be called if a file is updated and may be accessed again before the program exits
    """
    global cache
    cache.clear_path(path)


def cache_valid(path: str) -> bool:
    """
    Determines if the cache file at the given path is valid

    Returns true if and only if the cache file at the given path exists,
    the version of portmod is the same as the version stored in the cache file
    and that all file hashes in the cache file are valid
    """
    if not os.path.exists(path):
        return False

    with open(path, "r", encoding="utf-8") as cache_file:
        try:
            mod = json.load(cache_file)
        except Exception:
            return False

    if mod.get("__portmod_version__") != get_version():
        return False

    if not mod.get("__hashes__", []):
        return False

    for file, file_hash in mod.get("__hashes__"):
        if get_hash(file) != file_hash:
            return False

    return True


def pybuild_dumper(obj):
    # Serialize as best we can. Sets become lists and unknown objects are
    # just stringified
    if isinstance(obj, set):
        return list(obj)
    if hasattr(obj, "to_json"):
        return obj.to_json()
    return "{}".format(obj)


def create_cache_str(mod: FullPybuild, cache: bool = True) -> str:
    # Only include members declared in the Pybuild class.
    # Internal members should be ignored
    if mod.INSTALLED:
        dictionary = FullInstalledPybuild._to_cache(cast(FullInstalledPybuild, mod))
    else:
        dictionary = mod._to_cache()

    if cache:
        dictionary["__portmod_version__"] = get_version()

    for key in get_config()["CACHE_FIELDS"]:
        if hasattr(mod, key):
            dictionary[key] = getattr(mod, key)

    hashes = [(mod.FILE, get_hash(mod.FILE))]
    if cache:
        for super_cl in mod.__class__.mro():
            module = super_cl.__module__.split(".")
            # Note: All superclasses will be either in the pyclass directory,
            # portmod builtin superclasses, or builtin objects
            # We track v
            if module[0] != "pyclass":
                continue

            REPO_PATH = mod.REPO_PATH
            if mod.INSTALLED:
                REPO_PATH = get_repo(mod.REPO).location

            # Find path for pyclass module file
            filepath = os.path.join(REPO_PATH, *module) + ".py"
            dirpath = os.path.join(REPO_PATH, *module, "__init__.py")
            if os.path.exists(filepath):
                hashes.append((filepath, get_hash(filepath)))
                continue
            elif os.path.exists(dirpath):
                hashes.append((dirpath, get_hash(dirpath)))
                continue

            found = False
            for master in get_masters(REPO_PATH):
                filepath = os.path.join(master.location, *module) + ".py"
                dirpath = os.path.join(master.location, *module, "__init__.py")
                if os.path.exists(filepath):
                    hashes.append((filepath, get_hash(filepath)))
                    found = True
                    break
                elif os.path.exists(dirpath):
                    hashes.append((dirpath, get_hash(dirpath)))
                    found = True
                    break

            if not found:
                raise Exception(
                    f"Could not find path for module {super_cl.__module__} "
                    f"for mod {mod}"
                )

    dictionary["__hashes__"] = hashes
    return json.dumps(dictionary, default=pybuild_dumper, sort_keys=True)


def load_cache(path: str, installed: bool) -> Pybuild:
    # Don't try to load the pybuild if it previously failed this run
    if path in cache._failed:
        raise PreviouslyEncounteredException(cache._failed[path])

    atom = get_atom_from_path(path)
    repo_name = atom.R
    if installed:
        cache_file = os.path.join(env.prefix().PYBUILD_INSTALLED_CACHE, atom.C, atom.PF)
    else:
        cache_file = os.path.join(env.PYBUILD_CACHE_DIR, repo_name, atom.C, atom.PF)

    if not cache_valid(cache_file):
        from .loader import (
            LoadFromSandboxError,
            SandboxedError,
            _sandbox_execute_pybuild,
        )

        if env.SANDBOX:
            raise LoadFromSandboxError()

        os.makedirs(os.path.dirname(cache_file), exist_ok=True)

        if not path.endswith(".pybuild"):
            raise Exception()
        try:
            cache_str = _sandbox_execute_pybuild(
                path, "cache", Permissions(), installed=installed
            )
        except SandboxedError as e:
            cache._failed[path] = e
            raise e

        if not cache_str:
            err = Exception("Pybuild cache produced no output!")
            cache._failed[path] = err
            raise err
        with open(cache_file, "w", encoding="utf-8") as file:
            file.write(cache_str)

    with open(cache_file, "r", encoding="utf-8") as file:
        dictionary = json.load(file)
        return _load_cache_dict(path, atom, dictionary, installed)


def _load_cache_dict(file: str, atom: FQAtom, pkg: Dict, installed: bool) -> Pybuild:
    if installed:
        return InstalledPybuild(atom, cache=pkg, INSTALLED=installed, FILE=file)
    else:
        return Pybuild(atom, cache=pkg, INSTALLED=installed, FILE=file)


def __load_mod_from_dict_cache(file: str, *, installed=False) -> Pybuild:
    global cache
    dictionary = cache._mods

    if dictionary.get(file, False):
        return dictionary[file]
    else:
        mod = load_cache(file, installed)
        dictionary[file] = mod
        return mod
