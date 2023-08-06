# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for directly loading pybuild files.
These functions should not be called directly.
See portmod.loader for functions to load pybuilds safely using a sandbox.
"""

import ast
import glob
import importlib
import importlib.util
import os
import sys
from logging import warning
from types import SimpleNamespace
from typing import Any, Dict, Generator, Optional, cast

from RestrictedPython import (
    RestrictingNodeTransformer,
    compile_restricted_exec,
    limited_builtins,
    safe_globals,
)
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.Guards import (
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
    safer_getattr,
)

from portmod.atom import Atom, FQAtom, QualifiedAtom, VAtom, atom_sat
from portmod.functools import install_cache
from portmod.globals import env
from portmod.l10n import l10n
from portmod.lock import vdb_lock
from portmod.parsers.manifest import Manifest
from portmod.pybuild import FullInstalledPybuild, FullPybuild
from portmod.repo.metadata import get_categories
from portmod.util import get_max_version

from . import get_repo, get_repo_name
from .metadata import get_masters
from .updates import get_moved

WHITELISTED_IMPORTS = {
    "filecmp",
    "os",
    "sys",
    "shutil",
    "os.path",
    "chardet",
    "pybuild",
    "pybuild.info",
    "pybuild.winreg",
    "re",
    "csv",
    "json",
    "typing",
    "fnmatch",
    "collections",
    # FIXME: Remove eventually.
    # This is just to maintain compatibility with the current tree
    "pwinreg",
}
MODULE_WHITELISTED_IMPORTS = {
    "logging",
    "xml",
    "xml.dom",
    "xml.dom.minidom",
    "configparser",
    "portmod",
    "portmod.installed",
    "portmod.repo",
    "portmod.config",
    "portmod.repo.usestr",
    "portmod.tsort",
    "portmod.vfs",
    "portmod.module_util",
}

ALLOWED_IMPORTS = WHITELISTED_IMPORTS


def safe_import(
    _cache=None,
    extra_whitelist=set(),
    local_module_name=None,
    installed=False,
    repo=None,
):
    WHITELIST = WHITELISTED_IMPORTS | extra_whitelist
    cache = _cache or {}

    if env.PREFIX_NAME:
        # If the prefix is set, search all repositories
        # Otherwise, just search the particular repo (and masters)
        # containing this file.
        repo = None

    def _import_root(name, globs=None, loc=None, fromlist=(), level=0):
        def _import(name, globs=None, loc=None, fromlist=(), level=0):
            """
            Safe implementation of __import__ to use with RestrictedPython
            """
            if globs:
                if "__path__" in globs and level == 0:  # globs contains a module
                    module_name = globs["__name__"]
                else:  # Globs is a file, we want its parent
                    module_name = globs["__name__"].rpartition(".")[0]

                absolute_name = importlib.util.resolve_name(
                    level * "." + name, module_name
                )
            else:
                absolute_name = importlib.util.resolve_name(level * "." + name, "")

            path = None
            if "." in absolute_name:
                parent_name, _, child_name = absolute_name.rpartition(".")
                parent_module = _import(parent_name)
                path = parent_module.__spec__.submodule_search_locations

            if absolute_name in cache:
                return cache[absolute_name]

            # Note: using our custom code for whitelisted files has unintended side effects,
            # so we just import normally. See #135.
            if absolute_name in WHITELIST:
                module = __import__(name, globs, loc, fromlist, level)
                if "." in absolute_name:
                    cache[absolute_name] = getattr(parent_module, child_name)
                else:
                    cache[absolute_name] = module
                return cache[absolute_name]

            if (
                absolute_name in WHITELIST
                or absolute_name.startswith("pybuild")
                or absolute_name.startswith("common.")
                or absolute_name == "common"
                or (
                    local_module_name
                    and (
                        absolute_name == local_module_name
                        or absolute_name.startswith(local_module_name + ".")
                    )
                )
            ):
                if absolute_name == "common":
                    cache[absolute_name] = SimpleNamespace(
                        __spec__=SimpleNamespace(submodule_search_locations=[])
                    )
                    return cache[absolute_name]
                elif absolute_name.startswith("common."):
                    if len(absolute_name.split(".")) > 2:
                        raise Exception(f"Invalid package {absolute_name}")
                    _, module_name = absolute_name.split(".")
                    base_atom = Atom(f"common/{module_name}")
                    if installed:
                        path = find_installed_path(base_atom)

                    if installed and path:
                        module = SimpleNamespace(**__load_module(path, installed=True))
                    else:
                        versions = {}
                        for file in _iterate_pybuilds(base_atom, repo_name=repo):
                            atom, _ = os.path.splitext(file)
                            versions[
                                VAtom("common/" + os.path.basename(atom)).PVR
                            ] = file

                        max_version = get_max_version(versions.keys())
                        if not max_version:
                            raise Exception(f"Could not find package {absolute_name}")
                        module = SimpleNamespace(**__load_module(versions[max_version]))
                    if path is not None:
                        setattr(parent_module, child_name, module)
                    cache[absolute_name] = module
                    return module
                elif local_module_name and (
                    absolute_name == local_module_name
                    or absolute_name.startswith(local_module_name + ".")
                ):
                    spec = safe_find_spec(
                        absolute_name, path, cache, extra_whitelist, local_module_name
                    )
                    spec.loader = RestrictedLoader(
                        absolute_name,
                        spec.origin,
                        extra_whitelist,
                        local_module_name,
                        installed,
                    )
                    spec.loader.cache = cache  # type: ignore
                    module = importlib.util.module_from_spec(spec)
                else:
                    spec = importlib.util.find_spec(absolute_name, path)
                    spec.loader = importlib.machinery.SourceFileLoader(
                        absolute_name, spec.origin
                    )
                    module = importlib.util.module_from_spec(spec)
                if path is not None:
                    setattr(parent_module, child_name, module)
                cache[absolute_name] = module
                module.__loader__.exec_module(module)
                return module

            raise Exception(f"Unable to load restricted module {absolute_name}")

        return _import(name, globs, loc, fromlist, level)

    return _import_root


# Default implementation to handle invalid pybuilds
class Package:
    def __init__(self):
        raise Exception("Package is not defined")


def default_write_guard(ob):
    """
    Write guard that blocks modifications to modules
    """
    return ob


def safer_hasattr(obj, name):
    """
    Version of hasattr implemented using safet_getattr

    This doesn't really provide any extra security, but does mean that
    str.format, and attributes beginning with underscores, which are
    blocked by safer_getattr, return False rather than True
    """
    try:
        safer_getattr(obj, name)
    except (NotImplementedError, AttributeError):
        return False
    return True


def default_apply(func, *args, **kwargs):
    return func(*args, **kwargs)


SAFE_GLOBALS: Dict[str, Any] = safe_globals
SAFE_GLOBALS.update(
    {
        "Package": Package,
        "__metaclass__": type,
        "_getattr_": safer_getattr,
        "_getitem_": default_guarded_getitem,
        "_write_": default_write_guard,
        "_apply_": default_apply,
        "super": super,
        "_getiter_": default_guarded_getiter,
        "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
        "_unpack_sequence_": guarded_unpack_sequence,
        "FileNotFoundError": FileNotFoundError,
    }
)


class PrintWrapper:
    def __init__(self, _getattr_=None):
        self.txt = []
        self._getattr_ = _getattr_

    def write(self, text):
        self.txt.append(text)

    def __call__(self):
        return "".join(self.txt)

    def _call_print(self, *objects, **kwargs):
        if kwargs.get("file", None) is None:
            kwargs["file"] = sys.stdout
        else:
            self._getattr_(kwargs["file"], "write")
        print(*objects, **kwargs)


SAFE_GLOBALS["__builtins__"].update(
    {
        "_print_": PrintWrapper,
        "open": open,
        "set": set,
        "frozenset": frozenset,
        "hasattr": safer_hasattr,
        "getattr": safer_getattr,
        "next": next,
        "iter": iter,
        "filter": filter,
        "map": map,
        "max": max,
        "min": min,
        "dict": dict,
        "enumerate": enumerate,
        "sum": sum,
        "any": any,
        "all": all,
        "reversed": reversed,
        "sorted": sorted,
    }
)
SAFE_GLOBALS["__builtins__"].update(limited_builtins)


class Policy(RestrictingNodeTransformer):
    def visit_JoinedStr(self, node):
        return self.node_contents_visit(node)

    def visit_FormattedValue(self, node):
        return self.node_contents_visit(node)

    def visit_AnnAssign(self, node):
        return self.node_contents_visit(node)

    def visit_AugAssign(self, node):
        return self.node_contents_visit(node)

    def visit_ImportFrom(self, node):
        if (
            not node.module.startswith("common.")
            and node.module not in ALLOWED_IMPORTS
            and node.module not in MODULE_WHITELISTED_IMPORTS
            and not node.module.startswith("pybuild")
            and node.level == 0
        ):
            raise Exception(f"Not allowed to import from {node.module}")
        # For common, skip this restriction, since it will be loaded with
        # full restrictions in place. No unsafe modules will be available
        if not node.module.startswith("common.") and node.level == 0:
            try:
                module = importlib.import_module(node.module)
                for name in node.names:
                    if isinstance(module.__dict__.get(name.name), type(importlib)):
                        self.error(
                            node, "Importing modules from other modules is forbidden"
                        )
            except ModuleNotFoundError:
                pass

        return RestrictingNodeTransformer.visit_ImportFrom(self, node)

    def visit_Name(self, node):
        if node.id == "__PERMS":
            self.error(node, "Declaring i/o permissions is not allowed in the sandbox")
        return RestrictingNodeTransformer.visit_Name(self, node)

    def visit_FunctionDef(self, node):
        node = RestrictingNodeTransformer.visit_FunctionDef(self, node)
        if node.name == "__init__":
            newnode = ast.parse("super().__init__()").body[0]
            newnode.lineno = node.lineno
            newnode.col_offset = node.col_offset
            node.body.insert(0, newnode)
        return node


class RestrictedLoader(importlib.machinery.SourceFileLoader):
    def __init__(
        self,
        abs_name,
        origin,
        extra_whitelist=[],
        local_module_name=None,
        installed=False,
    ):
        super().__init__(abs_name, origin)
        self.extra_whitelist = extra_whitelist
        self.local_module_name = local_module_name
        self.installed = installed

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(module.__file__, "r", encoding="utf-8") as module_file:
            tmp_globals = SAFE_GLOBALS.copy()
            tmp_globals["__builtins__"]["__import__"] = safe_import(
                self.__dict__.get("cache", None),
                self.extra_whitelist,
                self.local_module_name,
                self.installed,
            )
            tmp_globals.update(module.__dict__)
            restricted_load(module_file.read(), module.__file__, tmp_globals)
            module.__dict__.update(tmp_globals)


def safe_find_spec(
    name,
    package=None,
    cache=None,
    extra_whitelist=[],
    local_module_name=None,
    installed=False,
):
    """
    Find a module's spec.
    Modified from importlib
    """

    def _find_spec(name, path, target=None):
        meta_path = sys.meta_path
        if meta_path is None:
            # PyImport_Cleanup() is running or has been called.
            raise ImportError("sys.meta_path is None, Python is likely shutting down")

        if not meta_path:
            warning("sys.meta_path is empty")

        for finder in meta_path:
            spec = None
            try:
                spec = finder.find_spec(name, path, target)
                if spec is not None:
                    return spec
            except AttributeError:
                loader = finder.find_module(name, path)
                if loader is not None:
                    spec = importlib.util.spec_from_loader(name, loader)
                    if spec is not None:
                        return spec
        else:
            return None

    fullname = (
        importlib.util.resolve_name(name, package) if name.startswith(".") else name
    )
    if fullname not in cache:
        parent_name = fullname.rpartition(".")[0]
        if parent_name:
            if parent_name in cache:
                parent = cache[parent_name]
            else:
                parent = safe_import(
                    cache, extra_whitelist, local_module_name, installed
                )(
                    parent_name,
                    globs=globals(),
                    fromlist=["__path__"],
                )
            try:
                parent_path = parent.__path__
            except AttributeError as error:
                raise ModuleNotFoundError(
                    f"__path__ attribute not found on {parent_name!r} "
                    f"while trying to find {fullname!r}",
                    name=fullname,
                ) from error
        else:
            parent_path = None
        return _find_spec(fullname, parent_path or package)

    module = cache[fullname]
    if module is None:
        return None
    try:
        spec = module.__spec__
    except AttributeError:
        raise ValueError("{}.__spec__ is not set".format(name)) from None
    else:
        if spec is None:
            raise ValueError("{}.__spec__ is None".format(name))
        return spec


def restricted_load(code, filepath, _globals):
    if sys.platform == "win32":
        code = code.replace("\\", "\\\\")
    byte_code, errors, warnings, names = compile_restricted_exec(
        code, filename=filepath, policy=Policy
    )
    if errors:
        raise SyntaxError(errors)
    seen: Dict[str, str] = {}
    for message in [seen.setdefault(x, x) for x in warnings if x not in seen]:
        if not message.endswith("Prints, but never reads 'printed' variable."):
            warning(f"In file {filepath}: {message}")
    exec(byte_code, _globals, _globals)


@install_cache
def get_atom_from_path(path: str) -> FQAtom:
    repopath, filename = os.path.split(os.path.abspath(os.path.normpath(path)))
    atom, _ = os.path.splitext(filename)
    repopath, _ = os.path.split(repopath)
    repopath, C = os.path.split(repopath)
    try:
        repo_name = get_repo_name(repopath)
    except FileNotFoundError as e:
        path = os.path.join(os.path.dirname(path), "REPO")
        if os.path.exists(path):
            with open(path, "r") as file:
                repo_name = file.read().strip() + "::installed"
        else:
            raise e
    return FQAtom(f"{C}/{atom}::{repo_name}")


def __load_module(path: str, *, installed=False) -> Dict[str, Any]:
    filename, _ = os.path.splitext(os.path.basename(path))
    repo = get_repo_name(path) if not installed else None

    with open(path, "r", encoding="utf-8") as file:
        code = file.read()
        tmp_globals = SAFE_GLOBALS.copy()
        tmp_globals["__builtins__"]["__import__"] = safe_import(
            installed=installed, repo=repo
        )
        tmp_globals["__name__"] = filename
        restricted_load(code, path, tmp_globals)

    return tmp_globals


def __load_file(path: str, *, installed=False) -> FullPybuild:
    """
    Loads a pybuild file

    :param path: Path of the pybuild file
    """
    module = __load_module(path, installed=installed)
    module["Package"].__pybuild__ = path
    mod = module["Package"]()
    mod.FILE = os.path.abspath(path)
    mod.INSTALLED = False

    if not installed:
        # determine common dependencies
        def find_common_imports(file: str):
            depends = []
            with open(file, "r", encoding="utf-8") as fp:
                tree = ast.parse(fp.read())

            def find_imports(tree: ast.AST):
                if isinstance(tree, ast.Module):
                    for statement in tree.body:
                        if isinstance(statement, ast.Import):
                            for alias in statement.names:
                                if alias.name.startswith("common."):
                                    depends.append(alias.name.replace(".", "/"))
                        elif isinstance(statement, ast.ImportFrom):
                            if statement.module and statement.module.startswith(
                                "common."
                            ):
                                depends.append(statement.module.replace(".", "/"))

            # Globals
            find_imports(tree)
            # TODO: Inline imports in functions?
            return depends

        mod.RDEPEND = " ".join([mod.RDEPEND] + find_common_imports(mod.FILE))
    return cast(FullPybuild, mod)


@vdb_lock()
def __load_installed(file: str) -> FullInstalledPybuild:
    """
    Loads an installed pybuild

    :param file: Path of the pybuild file
    """
    mod = cast(FullInstalledPybuild, __load_file(file, installed=True))
    mod.INSTALLED = True
    parent = os.path.dirname(file)

    def read_file(name: str) -> Optional[str]:
        if os.path.exists(os.path.join(parent, name)):
            with open(os.path.join(parent, name), "r") as repo_file:
                return repo_file.read().strip()
        return None

    repo = read_file("REPO")
    if not repo:
        raise Exception(
            f"Internal Error: Installed package in file {file}"
            "has no repository identifier"
        )
    mod.REPO = repo
    mod.INSTALLED_USE = set((read_file("USE") or "").split())
    mod.RDEPEND = read_file("RDEPEND") or mod.RDEPEND
    mod.INSTALLED_REBUILD_FILES = None
    path = os.path.join(parent, "REBUILD_FILES")
    if os.path.exists(path):
        try:
            mod.INSTALLED_REBUILD_FILES = Manifest(path)
        except ValueError:
            warning(f"Failed to load {path}")
            pass
    return mod


def _iterate_installed() -> Generator[str, None, None]:
    repo = env.prefix().INSTALLED_DB

    for path in glob.glob(os.path.join(repo, "*", "*", "*.pybuild")):
        yield path


def find_installed_path(atom: Atom) -> Optional[str]:
    repo_path = env.prefix().INSTALLED_DB

    # Handle renames:
    # Check all possible renames for this atom (all repos), and they are only valid if
    # the package comes from the repo matching the rename entry
    for repo in env.REPOS:
        moved = get_moved(repo)
        if atom.CPN in moved:
            moved_atom = QualifiedAtom(moved[atom.CPN])
            path = os.path.join(repo_path, moved_atom.C, moved_atom.PN)
            if os.path.exists(path):
                with open(os.path.join(path, "REPO"), "r") as file:
                    if repo.name == file.read().strip():
                        atom = moved_atom
                        break

    if atom.C:
        path = os.path.join(repo_path, atom.C, atom.PN)
        if os.path.exists(path):
            results = glob.glob(os.path.join(path, "*.pybuild"))
            assert len(results) == 1
            return results[0]
    else:
        for dirname in glob.glob(os.path.join(repo_path, "*")):
            path = os.path.join(repo_path, dirname, atom.PN)
            if os.path.exists(path):
                results = glob.glob(os.path.join(path, "*.pybuild"))
                assert len(results) == 1
                return results[0]
    return None


def _iterate_pybuilds(
    atom: Optional[Atom] = None, repo_name: Optional[str] = None
) -> Generator[str, None, None]:
    path = None
    repos = []
    if env.PREFIX_NAME:
        repos = env.prefix().REPOS
    else:
        repos = env.REPOS

    if repo_name is not None:
        repo = get_repo(repo_name)
        repos = [repo]
        for master in get_masters(repo.location):
            yield from _iterate_pybuilds(atom, master.name)

    def valid_atom(desired_atom: Atom, other: Atom):
        if isinstance(desired_atom, FQAtom):
            return desired_atom == other
        else:
            return atom_sat(other, desired_atom)

    def try_move_atom(moved: Dict[str, str], atom: QualifiedAtom, repo):
        true_atom = atom
        if atom.CPN in moved:
            true_atom = QualifiedAtom(moved[atom.CPN])
            if atom.PVR:
                true_atom = QualifiedAtom(f"{true_atom}-{atom.PVR}")
        return true_atom

    for repo in repos:
        if not os.path.exists(repo.location):
            warning(
                l10n(
                    "repo-does-not-exist-warning",
                    name=repo.name,
                    path=repo.location,
                    command="omwmerge --sync",
                )
            )

        if atom:
            moved = get_moved(repo)
            if atom.C:
                true_atom = try_move_atom(moved, cast(QualifiedAtom, atom), repo)
                path = os.path.join(repo.location, true_atom.C, true_atom.PN)
                if path is not None and os.path.exists(path):
                    for file in glob.glob(os.path.join(path, "*.pybuild")):
                        if valid_atom(true_atom, get_atom_from_path(file)):
                            yield file
            else:
                for category in get_categories(repo.location):
                    true_atom = try_move_atom(
                        moved, QualifiedAtom(category + "/" + atom), repo
                    )
                    path = os.path.join(repo.location, category, true_atom.PN)

                    if path is not None and os.path.exists(path):
                        for file in glob.glob(os.path.join(path, "*.pybuild")):
                            if valid_atom(true_atom, get_atom_from_path(file)):
                                yield file
        else:
            for file in glob.glob(os.path.join(repo.location, "*", "*", "*.pybuild")):
                yield file


def pkg_exists(atom: Atom, *, repo_name: Optional[str] = None) -> bool:
    """Returns true if a package with the given atom can be found in the given repository"""
    return next(_iterate_pybuilds(atom, repo_name), None) is not None
