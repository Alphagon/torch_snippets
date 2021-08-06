# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/paths.ipynb (unless otherwise specified).

__all__ = ['input_to_str', 'output_to_path', 'size', 'extn', 'Glob', 'sample', 'mv', 'cp', 'rm', 'P', 'isdir',
           'makedir', 'fname', 'fname2', 'stem', 'stems', 'parent', 'extn', 'Glob', 'find', 'zip_files', 'unzip_file',
           'md5', 'remove_duplicates', 'readlines', 'read_lines', 'writelines', 'write_lines', 'rename_batch',
           'dumpdill', 'loaddill', 'dill']

# Cell
from fastcore.basics import patch_to
from functools import wraps
from .logger import logger

def input_to_str(func):
    @wraps(func)
    def inner(input, *args, **kwargs):
        input = str(input)
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

# Cell
from .loader import choose as ts_choose
from pathlib import Path
P = Path
P.ls = lambda self: list(self.iterdir())
P.__repr__ = lambda self: f"» {self}"

@patch_to(P)
def size(self):
    if self.is_dir(): raise Exception(f"`{self}` is a directory")
    fsize = os.path.getsize(self) >> 20
    fsize = f'{fsize} MB' if fsize > 0 else f'{os.path.getsize(self) >> 10} KB'
    return fsize

@patch_to(P)
def extn(self, pattern='*'):
    return self.suffix.replace('.', '')

@patch_to(P)
def Glob(self, pattern='*'):
    return list(self.glob(pattern))

@patch_to(P)
def sample(self, pattern='*'):
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
def rm(self, confirm_prompt=True, verbose=True):
    confirm = input(f'Are you sure you want to delete `{self}`? [y/N]') if confirm_prompt else 'y'
    if confirm.lower() == 'y':
        os.remove(self)
        if verbose:
            logger.info(f'Deleted {self}')
    else:
        if verbose:
            logger.info(f'Aborting delete: {self}')

# Cell
import glob, os

def isdir(fpath): return os.path.isdir(fpath)

@input_to_str
def makedir(x):
    os.makedirs(x, exist_ok=True)

@input_to_str
def fname(fpath):
    return fpath.split('/')[-1]

@input_to_str
def fname2(fpath):
    return stem(fpath.split('/')[-1])

def stem(fpath):
    return P(fpath).stem

@input_to_str
def stems(folder):
    if isinstance(folder, (str, P)) : return [stem(str(x)) for x in Glob(folder)]
    if isinstance(folder, list): return [stem(x) for x in folder]

@input_to_str
@output_to_path
def parent(fpath):
    out = '/'.join(fpath.split('/')[:-1])
    if out == '': return './'
    else:         return out

def extn(x):
    return P(x).extn()

@input_to_str
@output_to_path
def Glob(x, extns=None, silent=False):
    files = glob.glob(x+'/*') if '*' not in x else glob.glob(x)
    if extns:
        if isinstance(extns, str): extns = extns.split(',')
        files = [f for f in files if any([f.endswith(ext) for ext in extns])]

    if not silent: logger.opt(depth=1).log('INFO', '{} files found at {}'.format(len(files), x))
    return files

def find(item, List, match_stem=False):
    '''Find an `item` in a `List`
    >>> find('abc', ['ijk','asdfs','dfsabcdsf','lmnop'])
    'dgsabcdsf'
    >>> find('file1', ['/tmp/file0.jpg', '/tmp/file0.png', '/tmp/file1.jpg', '/tmp/file1.png', '/tmp/file2.jpg', '/tmp/file2.png'])
    ['/tmp/file1.jpg', '/tmp/file1.png']
    '''
    filtered = [i for i in List if item in str(i)]
    if match_stem and len(filtered) > 1:
        filtered = [f for f in filtered if stem(f)==item]
    if len(filtered) == 1: return filtered[0]
    return filtered

# Cell
import zipfile
def zip_files(list_of_files, dest):
    import zipfile
    Info(f'Zipping {len(list_of_files)} files to {dest}...')
    with zipfile.ZipFile(dest, 'w') as zipMe:
        for file in Tqdm(list_of_files):
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

def unzip_file(file, dest):
    import zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dest)

# Cell
import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def remove_duplicates(files):
    hashes = [md5(f) for f in files]
    df = pd.DataFrame({'f':files, 'h': hashes})
    x = df.drop_duplicates('h')
    y = diff(files, x.f)
    for i in y:
        os.rename(i, './x')
    # !rm ./x
    return

# Cell
def readlines(fpath, silent=False, encoding=None):
    with open(fpath, 'r', encoding=encoding) as f:
        lines = f.read().split('\n')
        lines = [l.strip() for l in lines if l.strip()!='']
        if not silent: logger.opt(depth=1).log("INFO", f'loaded {len(lines)} lines')
        return lines

@patch_to(P)
def read_lines(self, silent=False, encoding=None):
    return readlines(self, silent=silent, encoding=encoding)

def writelines(lines, file):
    makedir(parent(file))
    failed = []
    with open(file, 'w') as f:
        for line in lines:
            try: f.write(f'{line}\n')
            except: failed.append(line)
    if failed!=[]:
        logger.opt(depth=1).log('INFO', f'Failed to write {len(failed)} lines out of {len(lines)}')
        return failed

@patch_to(P)
def write_lines(self, lines):
    return writelines(lines, self)

# Cell
def rename_batch(folder, func, debug=False, one_file=False):
    'V.V.Imp: Use debug=True first to confirm file name changes are as expected'
    if isinstance(folder, (str, P)): folder = Glob(folder)
    sources = []
    destins = []
    log_file = f'moved_files_{now()}.log'
    for f in folder:
        source = f
        destin = func(f)
        if source == destin: continue
        if debug:
            logger.debug(f'moving `{source}` --> `{destin}`')
        else:
            # !mv {source.replace(' ','\ ')} {destin.replace(' ','\ ')}
            logger.info(f'moving `{source}` --> `{destin}`')
            os.rename(source, destin)
        # !echo {source.replace(' ','\ ')} --\> {destin.replace(' ','\ ')} >> {logfile}
        if one_file: break

# Cell
import dill, time

dill = dill
def dumpdill(obj, fpath, silent=False):
    start = time.time()
    fpath = P(fpath)
    fpath.parent.mkdir(exist_ok=True)
    with open(fpath, 'wb') as f:
        dill.dump(obj, f)
    if not silent:
        fsize = fpath.size()
        logger.opt(depth=1).log('INFO', f'Dumped object of size ≈{fsize} @ "{fpath}" in {time.time()-start:.2e} seconds')

def loaddill(fpath):
    fpath = str(fpath)
    with open(fpath, 'rb') as f:
        obj = dill.load(f)
    return obj