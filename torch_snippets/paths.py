# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/paths.ipynb.

# %% auto 0
__all__ = ['P', 'dill', 'input_to_str', 'output_to_path', 'isdir', 'makedir', 'fname', 'fname2', 'stem', 'stems', 'parent',
           'extn', 'Glob', 'find', 'zip_files', 'unzip_file', 'md5', 'remove_duplicates', 'readlines', 'writelines',
           'rename_batch', 'dumpdill', 'loaddill']

# %% ../nbs/paths.ipynb 2
from fastcore.basics import patch_to
from functools import wraps
from .loader import choose as ts_choose, Tqdm, os, logger, Info, Debug, Warn, Excep
from pathlib import Path
import glob
import dill, time
import hashlib

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
P = Path
P.ls = lambda self: list(self.iterdir())
P.__repr__ = lambda self: f"» {self}"


@patch_to(P)
def size(self):
    if self.is_dir():
        raise Exception(f"`{self}` is a directory")
    fsize = os.path.getsize(self) >> 20
    fsize = f"{fsize} MB" if fsize > 0 else f"{os.path.getsize(self) >> 10} KB"
    return fsize


@patch_to(P)
def extn(self, pattern="*"):
    return self.suffix.replace(".", "")


@patch_to(P)
def Glob(self, pattern="*"):
    return list(self.glob(pattern))


@patch_to(P)
def sample(self, pattern="*"):
    return ts_choose(self.Glob(pattern))


@patch_to(P)
def mv(self, to):
    os.rename(self, to)
    return P(to)


import shutil


@patch_to(P)
def cp(self, to):
    return P(shutil.copy(self, to))


@patch_to(P)
def rm(self, confirm_prompt=False, silent=True, missing_ok=True):
    confirm = (
        input(f"Are you sure you want to delete `{self}`? [y/N]")
        if confirm_prompt
        else "y"
    )
    if confirm.lower() == "y":
        if missing_ok:
            try:
                os.remove(self)
            except:
                ...
        else:
            os.remove(self)
        if not silent:
            logger.info(f"Deleted {self}")
    else:
        if not silent:
            logger.info(f"Aborting delete: {self}")

# %% ../nbs/paths.ipynb 20
def isdir(fpath):
    return os.path.isdir(fpath)


@input_to_str
def makedir(x, prompt=False, silent=True):
    create = input(f'Creating folder {x}. Are you sure? [y/n]') if prompt else 'y'
    if create:
        os.makedirs(x, exist_ok=True)
    if not silent:
        Info(f'Created folder {x}')


@input_to_str
def fname(fpath):
    return fpath.split("/")[-1]


@input_to_str
def fname2(fpath):
    return stem(fpath.split("/")[-1])


def stem(fpath):
    return P(fpath).stem


@input_to_str
def stems(folder, silent=False):
    if isinstance(folder, (str, P)):
        return [stem(str(x)) for x in Glob(folder, silent=silent)]
    if isinstance(folder, list):
        return [stem(x) for x in folder]

P.stems = lambda self: stems(self.ls())

@input_to_str
@output_to_path
def parent(fpath):
    out = "/".join(fpath.split("/")[:-1])
    if out == "":
        return "./"
    else:
        return out


def extn(x):
    return P(x).extn()


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

# %% ../nbs/paths.ipynb 22
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

# %% ../nbs/paths.ipynb 24
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

# %% ../nbs/paths.ipynb 26
def readlines(fpath, silent=False, encoding=None):
    with open(fpath, "r", encoding=encoding) as f:
        lines = f.read().split("\n")
        lines = [l.strip() for l in lines if l.strip() != ""]
        if not silent:
            logger.opt(depth=1).log("INFO", f"loaded {len(lines)} lines")
        return lines


@patch_to(P)
def read_lines(self, silent=False, encoding=None):
    return readlines(self, silent=silent, encoding=encoding)


def writelines(lines, file):
    makedir(parent(file))
    failed = []
    with open(file, "w") as f:
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
def write_lines(self, lines):
    return writelines(lines, self)

# %% ../nbs/paths.ipynb 28
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

# %% ../nbs/paths.ipynb 29
dill = dill


def dumpdill(obj, fpath, silent=False):
    """Dump a python object as a dill file (better replacement to pickle)"""
    start = time.time()
    fpath = P(fpath)
    fpath.parent.mkdir(exist_ok=True)
    with open(fpath, "wb") as f:
        dill.dump(obj, f)
    if not silent:
        fsize = fpath.size()
        logger.opt(depth=1).log(
            "INFO",
            f'Dumped object of size ≈{fsize} @ "{fpath}" in {time.time()-start:.2e} seconds',
        )


def loaddill(fpath):
    """Load a python object from a dill file"""
    fpath = str(fpath)
    with open(fpath, "rb") as f:
        obj = dill.load(f)
    return obj
