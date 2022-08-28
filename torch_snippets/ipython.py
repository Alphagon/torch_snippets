# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/jupyter_notebook.ipynb (unless otherwise specified).

__all__ = ['is_in_notebook']

# Cell

import importlib
import os, sys

def is_in_notebook():
    try:
        # Test adapted from tqdm.autonotebook: https://github.com/tqdm/tqdm/blob/master/tqdm/autonotebook.py
        get_ipython = sys.modules["IPython"].get_ipython
        if "IPKernelApp" not in get_ipython().config:
            raise ImportError("console")

        return importlib.util.find_spec("IPython") is not None
    except (AttributeError, ImportError, KeyError):
        return False