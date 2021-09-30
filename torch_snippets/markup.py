# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/markups.ipynb (unless otherwise specified).

__all__ = ['isnamedtupleinstance', 'unpack', 'read_json', 'write_json', 'AttrDict', 'pretty_json', 'read_yaml',
           'write_yaml', 'Config']

# Cell
def isnamedtupleinstance(x):
    _type = type(x)
    bases = _type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(_type, '_fields', None)
    if not isinstance(fields, tuple):
        return False
    return all(type(i)==str for i in fields)

def unpack(obj):
    if isinstance(obj, dict):
        return {key: unpack(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [unpack(value) for value in obj]
    elif isnamedtupleinstance(obj):
        return {key: unpack(value) for key, value in obj._asdict().items()}
    elif isinstance(obj, tuple):
        return tuple(unpack(value) for value in obj)
    else:
        return obj


# Cell
import json
from .paths import *
from .logger import *

def read_json(fpath):
    import json
    with open(fpath, 'r') as f:
        return json.load(f)

def write_json(obj, fpath):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    logger.opt(depth=1).log("DEBUG", f"Dumping json to {fpath}")
    with open(fpath, "w") as f:
        json.dump(obj, f, indent=4, default=set_default)
    return P(fpath)

class AttrDict(object):
    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return AttrDict(value) if isinstance(value, dict) else value

    __getitem__ = lambda self, x: getattr(self, x)
    __setitem__ = lambda self, k, v: setattr(self, k, self._wrap(v))

    def __repr__(self):
        return '{%s}' % str(', '.join("'%s': %s" % (k, repr(v)) for (k, v) in self.__dict__.items()))

    def __dir__(self):
        return self.__dict__.keys()

    def to_dict(self):
        d = {}
        for k in dir(self):
            v = self[k]
            if isinstance(v, AttrDict):
                v = v.to_dict()
            d[k] = v
        return d

    def pretty(self, *args, **kwargs):
        pretty_json(self.to_dict(), *args, **kwargs)

    def __eq__(self, other):
        return AttrDict(other).to_dict() == self.to_dict()


def pretty_json(i, fpath=None, indent=4):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
    assert isinstance(i, (dict, list))
    i = unpack(i)
    dump = json.dumps(i, indent=indent, default=set_default)
    if fpath:
        makedir(parent(fpath))
        logger.info(f'Dumped a pretty file to {fpath}')
        with open(fpath, 'w') as f:
            json.dump(i, f, indent=indent, default=set_default)
            return
    return logger.opt(depth=1).log('DEBUG', f'\n{dump}')


# Cell
import yaml

def read_yaml(file):
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def write_yaml(content, fpath):
    with open(fpath, 'w') as outfile:
        yaml.dump(content, outfile, default_flow_style=False)

# Cell
from .thinc_parser.parser import Config
Config = Config