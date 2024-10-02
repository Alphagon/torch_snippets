# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/paths.ipynb.

# %% auto 0
__all__ = [
    "valid_methods",
    "P",
    "ls",
    "print_folder_summary",
    "dill",
    "input_to_str",
    "output_to_path",
    "process_f",
    "get_fs",
    "P0",
    "stem",
    "stems",
    "extn",
    "remove_file",
    "isdir",
    "makedir",
    "fname",
    "fname2",
    "parent",
    "Glob",
    "find",
    "zip_files",
    "unzip_file",
    "list_zip",
    "md5",
    "remove_duplicates",
    "common_items",
    "folder_summary",
    "readlines",
    "readfile",
    "writelines",
    "tree",
    "folder_structure_to_dict",
    "folder_structure_to_json",
    "rename_batch",
    "dumpdill",
    "loaddill",
]

# %% ../nbs/paths.ipynb 2
from fastcore.basics import patch_to
from fastcore.foundation import L
from pathlib import Path
from functools import wraps
from torch_snippets.loader import (
    choose as ts_choose,
    Tqdm,
    os,
    logger,
    Info,
    Debug,
    Warn,
    Excep,
    common,
)
from functools import lru_cache
import hashlib, shutil
from collections import defaultdict
import glob, json
import dill, time
import subprocess
import shutil


# %% ../nbs/paths.ipynb 3
def input_to_str(func):
    @wraps(func)
    def inner(input, *args, **kwargs):
        if isinstance(input, P):
            input = str(input)
        if isinstance(input, list):
            input = [str(i) for i in input]
        out = func(input, *args, **kwargs)
        return out

    return inner


def output_to_path(func):
    @wraps(func)
    def inner(input, *args, **kwargs):
        out = func(input, *args, **kwargs)
        if isinstance(out, str):
            out = P(out)
        if isinstance(out, list):
            if len(out) > 0 and isinstance(out[0], str):
                out = [P(o) for o in out]
        return out

    return inner


# %% ../nbs/paths.ipynb 4
def process_f(f):
    f = f.replace("-", "_").replace(".", "__")
    if f[0].isdigit():
        f = "_" + f

    return f


@lru_cache()
def get_fs(fldr):
    fldr = P(fldr)
    __fs = {f: stem(f) for f in fldr.ls()}
    _fs = defaultdict(list)
    for f, sf in __fs.items():
        _fs[sf].append(f)
    fs = {}
    for f, sfs in _fs.items():
        f = process_f(f)
        if len(sfs) == 1:
            fs[f] = sfs[0]
        else:
            for _f in sfs:
                fs[f"{f}__{_f.extn()}"] = _f
    return fs


valid_methods = dir(Path) + ["isfile"]


class P0(Path):
    try:
        from pathlib import _PosixFlavour, _WindowsFlavour

        _flavour = _PosixFlavour() if os.name == "posix" else _WindowsFlavour()
    except ImportError:
        pass

    def __new__(cls, *pathsegments):
        o = super().__new__(cls, *pathsegments)
        return o

    def __init__(self, *args, **kwargs):
        return super().__init__()

    @property
    @lru_cache()
    def isfile(self):
        return self.is_file()

    def ls(self):
        return L(self.iterdir())

    def extn(self, pattern="*"):
        return self.suffix.replace(".", "")

    def __getattr__(self, name):
        if name in valid_methods or self.isfile or self.exists():
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

        fs = get_fs(self)
        if name in fs:
            return fs[name]
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )


P = Path


@patch_to(P)
def Glob(self, pattern="*"):
    return L(self.glob(pattern))


def stem(fpath):
    return P(fpath).stem


@input_to_str
def stems(folder, silent=False):
    if isinstance(folder, (str, P)):
        return L([stem(str(x)) for x in Glob(folder, silent=silent)])
    if isinstance(folder, list):
        return L([stem(x) for x in folder])


P.stems = lambda self: stems(self.ls())
ls = lambda self: L(self.iterdir())
P.__repr__ = lambda self: f"» {self}"
P.__og_dir__ = P.__dir__


@patch_to(P)
def __dir__(self):
    if self.isfile:
        return self.__og_dir__()
    fs = get_fs(self)
    return self.__og_dir__() + list(fs.keys())


# %% ../nbs/paths.ipynb 8
@patch_to(P)
def rmtree(self, prompt="Really remove `{self}` and its contents? [y/n] ", force=False):
    if force:
        shutil.rmtree(self)
    elif prompt and input(prompt.format(self=self)).lower() == "y":
        shutil.rmtree(self)
    else:
        raise OSError(f"{self} exists and is not empty")


@patch_to(P)
def size(self):
    if self.is_dir():
        raise Exception(f"`{self}` is a directory")
    fsize = os.path.getsize(self) >> 20
    fsize = f"{fsize} MB" if fsize > 0 else f"{os.path.getsize(self) >> 10} KB"
    return fsize


@patch_to(P, as_prop=True)
def sz(self):
    return self.size()


@patch_to(P, as_prop=True)
def extn(self):
    return self.suffix.replace(".", "")


def extn(fpath):
    return P(fpath).extn


@patch_to(P)
def sample(self, pattern="*"):
    return ts_choose(self.Glob(pattern))


@patch_to(P)
def mv(self, to):
    os.rename(self, to)
    return P(to)


@patch_to(P)
def cp(self, to):
    return P(shutil.copy(self, to))


def remove_file(self, dry_run):
    if dry_run:
        print(f"DRY RUN: Removing {self}")
    else:
        os.remove(self)


@patch_to(P)
def rm(
    self,
    confirm_prompt="Are you sure you want to delete `{self}`? [y/N]",
    silent=True,
    missing_ok=True,
    force=False,
    dry_run=False,
):
    confirm = (
        input(confirm_prompt.format(self=self))
        if (confirm_prompt and not force)
        else "y"
    )
    if confirm.lower() == "y":
        if missing_ok:
            try:
                remove_file(self, dry_run)
            except:
                ...
        else:
            remove_file(self, dry_run)
        if not silent:
            logger.info(f"Deleted {self}")
    else:
        if not silent:
            logger.info(f"Aborting delete: {self}")


# %% ../nbs/paths.ipynb 21
def isdir(fpath):
    return os.path.isdir(fpath)


@input_to_str
def makedir(x, prompt=False, silent=True):
    create = input(f"Creating folder {x}. Are you sure? [y/n]") if prompt else "y"
    if create:
        os.makedirs(x, exist_ok=True)
    if not silent:
        Info(f"Created folder {x}")


@input_to_str
def fname(fpath):
    return fpath.split("/")[-1]


@input_to_str
def fname2(fpath):
    return stem(fpath.split("/")[-1])


@input_to_str
@output_to_path
def parent(fpath):
    out = "/".join(fpath.split("/")[:-1])
    if out == "":
        return "./"
    else:
        return out


@input_to_str
@output_to_path
def Glob(x, extns=None, silent=False):
    files = glob.glob(x + "/*") if "*" not in x else glob.glob(x)
    if extns:
        if isinstance(extns, str):
            extns = extns.split(",")
        files = [f for f in files if any([f.endswith(ext) for ext in extns])]

    # if not silent: logger.opt(depth=1).log('INFO', '{} files found at {}'.format(len(files), x))
    return files


def find(
    item=None, List=None, match_stem=False, condition=None, return_indexes_also=False
):
    """Find an `item` in a `List`
    >>> find('abc', ['ijk','asdfs','dfsabcdsf','lmnop'])
    'dgsabcdsf'
    >>> find('file1', ['/tmp/file0.jpg', '/tmp/file0.png', '/tmp/file1.jpg', '/tmp/file1.png', '/tmp/file2.jpg', '/tmp/file2.png'])
    ['/tmp/file1.jpg', '/tmp/file1.png']
    """
    if callable(condition):
        filtered = [(ix, i) for ix, i in enumerate(List) if condition(i)]

    else:
        filtered = [(ix, i) for ix, i in enumerate(List) if item in str(i)]

    if match_stem and len(filtered) > 1:
        filtered = [(ix, f) for ix, f in filtered if stem(f) == item]

    if len(filtered) == 1:
        if return_indexes_also:
            return filtered[0]
        else:
            return filtered[0][1]
    elif len(filtered) == 0:
        return None
    else:
        ixs, filtered_items = list(zip(*filtered))
        if return_indexes_also:
            return ixs, filtered_items
        else:
            return filtered_items


# %% ../nbs/paths.ipynb 23
import zipfile
import tarfile


def zip_files(list_of_files, dest):
    dest = str(dest)
    logger.info(f"Zipping {len(list_of_files)} files to {dest}...")
    if dest.lower().endswith(".zip"):
        with zipfile.ZipFile(dest, "w") as zipMe:
            for file in Tqdm(list_of_files):
                zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
    elif dest.lower().endswith(".tar.gz"):
        with tarfile.open(dest, "w:gz") as tarMe:
            for file in Tqdm(list_of_files):
                tarMe.add(file)
    return P(dest)


def unzip_file(file, dest):
    file = str(file)
    if file.lower().endswith(".zip"):
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(dest)
    elif file.lower().endswith(".tar.xz") or file.endswith(".tar.gz"):
        with tarfile.open(file, "r") as f:
            f.extractall(dest)
    return P(dest)


def list_zip(file):
    elements = []
    with zipfile.ZipFile(file, "r") as zipObj:
        listOfiles = zipObj.namelist()
        for elem in listOfiles:
            elements.append(elem)
    return elements


# %% ../nbs/paths.ipynb 25
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_duplicates(files):
    """Check a list of files and remove duplicates based on their checksum"""
    import pandas as pd
    from torch_snippets.loader import diff

    hashes = [md5(f) for f in files]
    df = pd.DataFrame({"f": files, "h": hashes})
    x = df.drop_duplicates("h")
    y = diff(files, x.f)
    for i in y:
        os.rename(i, "./x")
    # !rm ./x
    return


def common_items(*fldrs, verbose=True):
    fldr_items = [stems(fldr) for fldr in fldrs]
    o = sorted(common(*fldr_items))
    if verbose:
        Info(
            f"Returning {len(o)} common items from folders of {[len(_f) for _f in fldr_items]} items each"
        )
    return o


def folder_summary(thing):
    things = Glob(thing)
    info = []
    for thing in things:
        if thing.is_dir():
            info.append(f"{thing} - {len(Glob(thing))} items")
        else:
            info.append(f"{thing} - {thing.size()}")
    return "\n".join(info)


print_folder_summary = lambda x: print(folder_summary(x))


# %% ../nbs/paths.ipynb 27
def readlines(fpath, silent=False, encoding=None, _strip=True):
    with open(fpath, "r", encoding=encoding) as f:
        lines = f.read().split("\n")
        if _strip:
            lines = [l.strip() for l in lines if l.strip() != ""]
        if not silent:
            logger.opt(depth=1).log("INFO", f"loaded {len(lines)} lines")
        return lines


@patch_to(P)
def read_lines(self, silent=False, encoding=None):
    return readlines(self, silent=silent, encoding=encoding)


def readfile(*args, **kwargs):
    kwargs.pop("_strip", None)
    return "\n".join(readlines(*args, _strip=False, **kwargs)).strip()


@patch_to(P)
def read_file(self, **kwargs):
    return readfile(self, **kwargs)


def writelines(lines, file, mode):
    makedir(parent(file))
    failed = []
    with open(file, mode) as f:
        for line in lines:
            try:
                f.write(f"{line}\n")
            except:
                failed.append(line)
    if failed != []:
        logger.opt(depth=1).log(
            "INFO", f"Failed to write {len(failed)} lines out of {len(lines)}"
        )
        return failed


@patch_to(P)
def write_lines(self, lines, mode):
    return writelines(lines, self, mode)


# %% ../nbs/paths.ipynb 29
def tree(directory="./", filelimit=50, to=None):
    from builtins import print

    # Construct the shell command
    directory = str(P(directory).resolve())
    shell_command = f"tree \"{directory}\" --filelimit={filelimit} | sed 's/├/ /g; s/└/ /g; s/|/ /g; s/`/ /g; s/│/ /g; s/+/ /g'"
    # Execute the shell command
    try:
        result = subprocess.run(
            shell_command, shell=True, capture_output=True, text=True
        )
        # Print the output
        if to:
            writelines(result.stdout.split("\n"), to, mode="w")
        else:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")


@patch_to(P, as_prop=True)
def _tree(self, filelimit=50, to=None):
    return tree(self, filelimit, to)


P.tree = P._tree


# %% ../nbs/paths.ipynb 31
def folder_structure_to_dict(path):
    """
    Recursively constructs a nested dictionary that represents the folder structure.
    """
    folder_dict = {}
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                folder_dict[entry.name] = folder_structure_to_dict(entry.path)
            else:
                folder_dict[entry.name] = None
    return folder_dict


def folder_structure_to_json(path, output_file=None):
    """
    Creates a JSON file representing the folder structure of the given directory.
    """
    path = P(path)
    if output_file is None:
        output_file = path / "tree.json"
    folder_dict = folder_structure_to_dict(path)
    with open(output_file, "w") as f:
        json.dump(folder_dict, f, indent=4)


# %% ../nbs/paths.ipynb 33
def rename_batch(folder, func, debug=False, one_file=False):
    from torch_snippets.loader import now

    "V.V.Imp: Use debug=True first to confirm file name changes are as expected"
    if isinstance(folder, (str, P)):
        folder = Glob(folder)
    sources = []
    destins = []
    log_file = f"moved_files_{now()}.log"
    for f in folder:
        source = f
        destin = func(f)
        if source == destin:
            continue
        if debug:
            logger.debug(f"moving `{source}` --> `{destin}`")
        else:
            # !mv {source.replace(' ','\ ')} {destin.replace(' ','\ ')}
            logger.info(f"moving `{source}` --> `{destin}`")
            os.rename(source, destin)
        # !echo {source.replace(' ','\ ')} --\> {destin.replace(' ','\ ')} >> {logfile}
        if one_file:
            break


# %% ../nbs/paths.ipynb 34
dill = dill


def dumpdill(
    obj,
    fpath,
    silent=False,
    message='Dumped object of size ≈{fsize} @ "{fpath}" in {dumptime:.2e} seconds',
):
    """Dump a python object as a dill file (better replacement to pickle)"""
    start = time.time()
    fpath = P(fpath)
    fpath.parent.mkdir(exist_ok=True, parents=True)
    with open(fpath, "wb") as f:
        dill.dump(obj, f)
    dumptime = time.time() - start
    if not silent:
        fsize = fpath.size()
        logger.opt(depth=1).log(
            "INFO", message.format(fsize=fsize, fpath=fpath, dumptime=dumptime)
        )
    return P(fpath)


def loaddill(fpath):
    """Load a python object from a dill file"""
    fpath = str(fpath)
    with open(fpath, "rb") as f:
        obj = dill.load(f)
    return obj
