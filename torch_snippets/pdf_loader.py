# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/pdf.ipynb.

# %% auto 0
__all__ = ["PDF"]

# %% ../nbs/pdf.ipynb 2
from .loader import np, subplots, show, resize, L, Image
from fastcore.basics import ifnone
import fitz

# %% ../nbs/pdf.ipynb 3
class PDF:
    """Load a PDF file from `path` as a list of images
    Use `show` function to see the images
    **WIP**"""

    def __init__(self, path, dfs=None, dpi=150):
        self.path = path
        self.dpi = dpi
        self.doc = fitz.open(path)
        self.ims = L([self.get_image(page_no) for page_no in range(len(self))])
        self.dfs = L(dfs) if dfs is not None else L([None] * len(self))

    def get_image(self, page_no, dpi=None):
        page = self.doc.load_page(page_no)
        pix = page.get_pixmap(dpi=ifnone(dpi, self.dpi))
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        return img

    def __len__(self):
        return len(self.doc)

    def __getitem__(self, ix):
        return self.ims[ix]

    def show(self, ix=None, ixs=None, **kwargs):
        if ixs is not None:
            assert isinstance(ixs, (list, L))
            subplots(L(self.ims)[ixs], **kwargs)
        if ix is not None:
            show(self.ims[ix], **kwargs)
            return

        if len(self) == 1:
            show(self.ims[0], df=self.dfs[0], **kwargs)
        else:
            subplots(self.ims, dfs=self.dfs, **kwargs)
