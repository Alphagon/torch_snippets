# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/markups.ipynb (unless otherwise specified).

__all__ = ['read_json', 'write_json', 'AttrDict', 'pretty_json']

# Cell
import json
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

class AttrDict(dict):
    MARKER = object()

    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError('expected dict')

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            value = AttrDict(value)
        super(AttrDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        found = self.get(key, AttrDict.MARKER)
        if found is AttrDict.MARKER:
            found = AttrDict()
            super(AttrDict, self).__setitem__(key, found)
        return found

    __setattr__, __getattr__ = __setitem__, __getitem__

    def to_dict(self):
        d = {}
        for k in self.keys():
            v = self[k]
            if isinstance(v, AttrDict):
                v = v.to_dict()
            d[k] = v
        return d

    def pretty(self, *args, **kwargs):
        pretty_json(self.to_dict(), *args, **kwargs)


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