# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/markups.ipynb.

# %% auto 0
__all__ = [
    "AD",
    "Config",
    "isnamedtupleinstance",
    "unpack",
    "AttrDict",
    "pretty_json",
    "read_json",
    "write_json",
    "write_jsonl",
    "read_jsonl",
    "read_yaml",
    "write_yaml",
    "read_xml",
    "write_xml",
]

import hashlib

# %% ../nbs/markups.ipynb 2
import json
import os
from collections.abc import Mapping
from json import JSONEncoder
from typing import Union

import jsonlines
import xmltodict
import yaml

from .icecream import ic
from .loader import BB, L, np, pd
from .logger import *
from .paths import *
from .thinc_parser.parser import Config


# %% ../nbs/markups.ipynb 3
def _default(self, obj):
    return getattr(obj.__class__, "__json__", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


def isnamedtupleinstance(x):
    _type = type(x)
    bases = _type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(_type, "_fields", None)
    if not isinstance(fields, tuple):
        return False
    return all(type(i) == str for i in fields)


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


def hash_tensor(tensor):
    import torch

    assert isinstance(tensor, torch.Tensor)
    try:
        tensor_str = tensor.cpu().detach().numpy().tobytes()
    except:
        ...
    hash_obj = hashlib.sha256(tensor_str)
    return "ID:#" + hash_obj.hexdigest()[:6]


def hash_pandas_dataframe(input):
    try:
        from pandas.util import hash_pandas_object

        h = hash_pandas_object(input, index=True).values
        return "ID:#" + hashlib.sha256(h).hexdigest()[:6]
    except:
        return "ID:#<uncomputable>"


class AttrDict(object):
    """
    Utility class to interact with a dictionary as if it were an object. `AD` is an alias to this class

    FEATURES:
    0. Access and modify keys (including nested keys) as if they were object attributes, supporting tab-completion.
       Example: `self.key1.key2[0].key3`
    1. Keys and values are recursively converted to AttrDict instances.
    2. Pretty-print the dictionary using `print`.
    3. Convert the entire structure to a regular dictionary at any time using `self.to_dict() / self.dict()`.
    3. Recursively remove keys using `self.drop(key)` from a JSON object.
    4. Apply a function to all values at all levels using `map`.

    GOTCHAS:
    1. All integer keys are implicitly converted to strings due to the enforced `self.key` format.
    2. You can still use `self[int]`, but this internally converts the integer to a string.

    METHODS:
    - `items()`: Return the items of the AttrDict as key-value pairs.
    - `keys()`: Return the keys of the AttrDict.
    - `values()`: Return the values of the AttrDict.
    - `update(dict)`: Update the AttrDict with key-value pairs from another dictionary.
    - `get(key, default=None)`: Get the value associated with a key, with an optional default value.
    - `__iter__()`: Allow iteration over the keys of the AttrDict.
    - `__len__()`: Return the number of keys in the AttrDict.
    - `__repr__()`: Return a string representation of the AttrDict.
    - `__dir__()`: List the keys of the AttrDict as attributes.
    - `__contains__(key)`: Check if a key exists in the AttrDict, use 'a.b.c' notation to directly check for a nested attribute.
    - `__delitem__(key)`: Delete a key from the AttrDict.
    - `map(func)`: Apply a function to all values in the AttrDict.
    - `drop(key)`: Recursively remove a key and its values from the AttrDict.
    - `to_dict()`: Convert the AttrDict and its nested structure to a regular dictionary.
    - `pretty(print_with_logger=False, *args, **kwargs)`: Pretty-print the AttrDict as JSON.
    - `__eq__(other)`: Compare the AttrDict with another dictionary for equality.
    - `find_address(key, current_path="")`: Find and return all addresses (paths) of a given key in the AttrDict.
    - `summary(current_path='', summary_str='', depth=0, sep='\t')`: Generate a summary of the structure and values in the AttrDict.
    - `write_summary(to, **kwargs)`: Write the summary to a file or stream.
    - `fetch(addr)`: Retrieve a value at a specified address (path).

    PARAMETERS:
    - `data` (dict, optional): Initial data to populate the AttrDict.

    USAGE:
    - Create an AttrDict instance by providing an optional initial dictionary, and then access and manipulate its contents as if they were object attributes.

    EXAMPLE:
    ```python
    my_dict = {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}
    attr_dict = AttrDict(my_dict)
    print(attr_dict.name)  # Access values like attributes
    attr_dict.address.city = 'Los Angeles'  # Modify nested values
    ```
    """

    forbidden = set(":,'\"}{.")

    def __init__(self, *args, given_input_to_ad=None, **kwargs):
        given_input_to_ad = {} if given_input_to_ad is None else given_input_to_ad
        if len(args) == 1 and isinstance(args[0], (Mapping, AttrDict)):
            given_input_to_ad = args[0]
            args = {}
        else:
            _args = dict(ic.io(*args)) if len(args) > 0 else {}
            args = {}
            for k, v in _args.items():
                if any(c in self.forbidden for c in k):
                    assert isinstance(
                        v, (dict, AttrDict)
                    ), f"Input `{v}` can't be a list"
                    given_input_to_ad = {**v, **given_input_to_ad}
                else:
                    args = {**{k: v}, **args}

        given_input_to_ad = {**kwargs, **given_input_to_ad, **args}
        for name, value in given_input_to_ad.items():
            setattr(self, str(name), self._wrap(value))

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def _wrap(self, value):
        if isinstance(value, (L, tuple, list, set, frozenset)):
            value = type(value)([self._wrap(v) for v in value])
            if isinstance(value, (list, L)):
                value = L(value)
            return value
        else:
            return (
                AttrDict(given_input_to_ad=value) if isinstance(value, dict) else value
            )

    __getitem__ = lambda self, x: (
        AttrDict({_x: self[_x] for _x in x})
        if isinstance(x, (list, L))
        else getattr(self, str(x))
    )
    __setitem__ = lambda self, k, v: setattr(self, str(k), self._wrap(v))

    def update(self, dict):
        for k, v in dict.items():
            self[k] = v

    def get(self, key, default=None):
        key = str(key)
        return self[key] if key in self else default

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __repr__(self):
        return f"\n```↯ AttrDict ↯\n{self.summary()}\n```\n"

    def __dir__(self):
        return self.__dict__.keys()

    def __contains__(self, key):
        key = str(key)
        if "." not in key:
            return key in self.__dict__.keys()
        else:
            d = self
            for _k in key.split("."):
                try:
                    d = d[_k]
                except AttributeError:
                    return False
            return True

    def __delitem__(self, key):
        key = str(key)
        del self.__dict__[key]

    def map(self, func):
        for k in dir(self):
            v = self[k]
            if isinstance(v, AttrDict):
                v.map(func)
            elif isinstance(v, (L, tuple, list, set, frozenset)):
                v = [_v.map(func) if isinstance(_v, AttrDict) else func(_v) for _v in v]
            else:
                v = func(v)
            self[k] = v

    def drop(self, key):
        if key in self:
            del self[key]
        for k in dir(self):
            v = self[k]
            if isinstance(v, AttrDict):
                v.drop(key)
            if isinstance(v, (L, tuple, list, set, frozenset)):
                v = [_v.drop(key) for _v in v if isinstance(_v, AttrDict)]

    def to_dict(self):
        d = {}
        for k in dir(self):
            v = self[k]
            if isinstance(v, AttrDict):
                v = v.to_dict()
            if isinstance(v, (L, tuple, list, set, frozenset)):
                v = [_v.to_dict() if isinstance(_v, AttrDict) else _v for _v in v]
            d[k] = v
        return d

    def pretty(self, print_with_logger=False, *args, **kwargs):
        pretty_json(
            self.to_dict(), print_with_logger=print_with_logger, *args, **kwargs
        )

    def __eq__(self, other):
        return AttrDict(given_input_to_ad=other).to_dict() == self.to_dict()

    def find_address(self, key, current_path=""):
        addresses = []
        for k in self.keys():
            if current_path:
                new_path = f"{current_path}.{k}"
            else:
                new_path = k

            if k == key:
                addresses.append(new_path)

            if isinstance(self[k], AttrDict):
                addresses.extend(self[k].find_address(key, new_path))

            elif isinstance(self[k], (L, tuple, list, set, frozenset)):
                for i, item in enumerate(self[k]):
                    if isinstance(item, AttrDict):
                        addresses.extend(item.find_address(key, f"{new_path}.{i}"))
        return addresses

    def summary(self, current_path="", depth=0, sep="  ", max_items=10):
        max_items = int(os.environ.get("AD_MAX_ITEMS", max_items))
        sep = os.environ.get("AD_SEP", sep)

        def format_path(path, key):
            return f"{path}.{key}" if path else key

        def format_item(key, item, path, depth, sep):
            import numpy as np
            import pandas as pd

            try:
                import torch
            except ModuleNotFoundError:

                class Torch:
                    Tensor = type(None)

                torch = Torch()

            if isinstance(item, (pd.DataFrame,)):
                return f"{sep * depth}{key} - {type(item).__name__} - shape {item.shape} - columns {item.columns} - {hash_pandas_dataframe(item)}\n"
            if isinstance(item, AttrDict) or hasattr(item, "keys"):
                item = AttrDict(**item)
                return f"{sep*depth}{key}\n" + item.summary(path, depth + 1, sep)
            elif isinstance(item, (list, tuple, set, frozenset, L)):
                return summarize_collection(key, item, path, depth + 1, sep)
            elif isinstance(item, (torch.Tensor, np.ndarray)):
                is_np = False
                if isinstance(item, np.ndarray):
                    is_np = True
                    item = torch.tensor(item)
                is_np = "🔦" if not is_np else "np."
                return f"{sep * depth}{key} - {is_np}{item} - {hash_tensor(item)}\n"

            else:
                if isinstance(item, (int, float, complex, str, P)):
                    is_multiline = False
                    ogitem = item
                    if isinstance(item, (str, P)):
                        is_multiline = "\n" in item
                        _sep = (
                            " ...\n...\n...\n...\n... " if is_multiline else "........."
                        )
                        if len(item) > 100:
                            item = item[:35] + _sep + item[-35:]
                        if is_multiline:
                            _item = item.split("\n")
                            _item = "\n".join([f"{sep*(depth+1)}{l}" for l in _item])
                            item = f"↓\n{sep*(depth+1)}```\n{_item}\n{sep*(depth+1)}```"
                    multiline = "" if not is_multiline else "Multiline "
                    return f"{sep * depth}{key} - {item} ({multiline}{type(ogitem).__name__})\n"
                else:
                    return f"{sep * depth}{key} - {type(item).__name__}\n"

        def summarize_collection(key, collection, path, d, s):
            summary_str = f"{s * (d - 1)}{key}\n"
            for i, item in enumerate(collection):
                item_path = format_path(path, i)
                if i < max_items:
                    summary_str += format_item(i, item, item_path, d, s)
                else:
                    summary_str += (
                        f"{s*d}... {len(collection) - max_items} more items ...\n"
                    )
                    break
            return summary_str

        summary_str = ""
        for ix, key in enumerate(self.keys()):
            if ix >= max_items:
                summary_str += (
                    f"{sep*depth} ... {len(self.keys()) - max_items} more keys ...\n"
                )
                break
            new_path = format_path(current_path, key)
            summary_str += format_item(key, self[key], new_path, depth, sep)
        return summary_str

    def print_summary(self, **kwargs):
        from builtins import print

        print(self.summary(**kwargs))

    def write_summary(self, to, **kwargs):
        writelines(self.summary(**kwargs).split("\n"), to)

    def fetch(self, addr):
        if isinstance(addr, (list, L)):
            return L([self.fetch(_addr) for _addr in addr])

        o = self
        for p in addr.split("."):
            try:
                o = o[int(p)]
            except:
                o = o[p]
        return o


AD = AttrDict
AD.dict = AD.to_dict


def pretty_json(
    i, fpath=None, indent=4, print_with_logger=True, return_as_string=False
):
    def set_default(obj):
        if isinstance(obj, (set, BB, L)):
            return list(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, P):
            return str(obj)

    assert isinstance(i, (dict, list))
    i = unpack(i)
    dump = json.dumps(i, indent=indent, default=set_default)
    if fpath:
        makedir(parent(fpath))
        logger.info(f"Dumped a pretty file to {fpath}")
        with open(fpath, "w") as f:
            json.dump(i, f, indent=indent, default=set_default)
            return
    if print_with_logger:
        return logger.opt(depth=1).log("DEBUG", f"\n{dump}")
    else:
        if return_as_string:
            return dump
        print(dump)


# %% ../nbs/markups.ipynb 8
def read_json(fpath):
    import json

    with open(fpath, "r") as f:
        return json.load(f)


def write_json(obj, fpath, silent=False):
    from datetime import date, datetime

    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError

    if not silent:
        logger.opt(depth=1).log("DEBUG", f"Dumping json to {fpath}")
    with open(fpath, "w") as f:
        json.dump(obj, f, indent=4, default=set_default)
    return P(fpath)


# %% ../nbs/markups.ipynb 10
def write_jsonl(items, dest, mode="a"):
    makedir(parent(dest))
    with jsonlines.open(dest, mode) as writer:
        writer.write_all(items)
        if mode == "a":
            Info(f"Appended {len(items)} items to {dest}")
        elif mode == "w":
            Info(f"Wrote {len(items)} jsons to {dest}")


def read_jsonl(file):
    return [json.loads(line) for line in readlines(file, silent=True)]


# %% ../nbs/markups.ipynb 11
def read_yaml(file):
    with open(file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_yaml(content, fpath):
    with open(fpath, "w") as outfile:
        yaml.dump(content, outfile, default_flow_style=False)


# %% ../nbs/markups.ipynb 12
def read_xml(file_path: Union[str, P]) -> AttrDict:
    "Read xml data as a dictionary"
    with open(str(file_path)) as xml_file:
        data = AttrDict(given_input_to_ad=xmltodict.parse(xml_file.read()))
    return data


def write_xml(data: Union[AttrDict, dict], file_path: Union[str, P]):
    makedir(parent(file_path))
    "convert a dictionary to xml"
    with open(file_path, "w") as xml_file:
        data = data.to_dict() if isinstance(data, AttrDict) else data
        assert isinstance(data, dict), "Function only supports dicts for now"
        data = xmltodict.unparse(data, pretty=True)
        xml_file.write(data)


def decompose(i):
    print(
        AD(
            {k: getattr(i, k) for k in dir(i) if not k.startswith("_")},
            type=str(type(i)),
        )
    )


# %% ../nbs/markups.ipynb 13
Config = Config

if __name__ == "__main__":
    assert AD({}) == {}

    p = 1
    q = {"a": 10}
    s = AD(p, q, a=20, b=30)
    assert s == {"a": 20, "b": 30, "p": 1, "q": {"a": 10}}

    s = AD(p, **q, b=30)
    assert s == {"a": 10, "b": 30, "p": 1}

    p = {"b": 222}
    assert AD(p, {"a": 2, "b": 2}, {"bb": 2, "a": 3, "b": 3}, a=20, b=30) == {
        "a": 2,
        "b": 2,
        "bb": 2,
        "p": {"b": 222},
    }

    d1 = {"c": 1}
    d2 = {"c": 2}
    d3 = {"c": 3}
    l = [1, 2, 3]
    assert AD(l, {"c": 100}, d1, d2, d3, d1={"c": 10}, d2={"c": 20}).to_dict() == {
        "l": [1, 2, 3],
        "d1": {"c": 1},
        "d2": {"c": 2},
        "c": 100,
        "d3": {"c": 3},
    }

    a = 20
    b = 30
    assert AD(a, b).to_dict() == {"a": 20, "b": 30}

    p = 10
    q = {"a": 1}
    assert AD(p, q) == {"p": 10, "q": {"a": 1}}
    assert AD(p, {"a": 1}) == {"p": 10, "a": 1}

    x = {"a": 1, "b": 2, "c": 3}
    assert AD(x).to_dict() == {"x": {"a": 1, "b": 2, "c": 3}}
    assert AD(**x).to_dict() == {"a": 1, "b": 2, "c": 3}
