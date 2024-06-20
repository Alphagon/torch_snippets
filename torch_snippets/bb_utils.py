# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/bounding_boxes.ipynb.

# %% auto 0
__all__ = ['randint', 'BB', 'df2bbs', 'bbs2df', 'bbfy', 'jitter', 'compute_eps', 'enlarge_bbs', 'shrink_bbs', 'iou',
           'compute_distance_matrix', 'compute_distances', 'split_bb_to_xyXY', 'combine_xyXY_to_bb', 'is_absolute',
           'is_relative', 'to_relative', 'to_absolute', 'merge_by_bb', 'isin']

# %% ../nbs/bounding_boxes.ipynb 2
import numpy as np
import pandas as pd
from PIL.Image import Image
from typing import Tuple

# %% ../nbs/bounding_boxes.ipynb 3
randint = np.random.randint


class BB:
    """A Bounding Box defined by the top-left and bottom-right coordinates"""

    def __init__(self, *bb):
        # assert len(bb) == 4, 'expecting a list/tuple of 4 values respectively for (x,y,X,Y)'
        if len(bb) == 4:
            x, y, X, Y = bb
        elif len(bb) == 1:
            ((x, y, X, Y),) = bb
        rel = True if max(x, y, X, Y) < 1 else False
        # if not rel:
        #    x, y, X, Y = map(lambda i: int(round(i)), (x, y, X, Y))
        self.bb = x, y, X, Y
        self.x, self.y, self.X, self.Y = x, y, X, Y
        self.xc, self.yc = (self.x + self.X) / 2, (self.y + self.Y) / 2
        self.c = (self.xc, self.yc)
        self.h = Y - y
        self.w = X - x
        self.area = self.h * self.w
        self.shape = (self.h, self.w)

    def __getitem__(self, i):
        return self.bb[i]

    def __repr__(self):
        return self.bb.__repr__()

    def __len__(self):
        return 4

    def __eq__(self, other):
        return (
            self.x == other.x
            and self.y == other.y
            and self.X == other.X
            and self.Y == other.Y
        )

    def __hash__(self):
        return hash(tuple(self))

    def __add__(self, origin):
        a, b = origin[:2]
        x, y, X, Y = self
        return BB(x + a, y + b, X + a, Y + b)

    def remap(self, og_dim: Tuple[int, int], new_dim: Tuple[int, int]):
        """
        og_dim = (Height, Width)
        new_dim = (Height, Width)
        """
        h, w = og_dim
        H, W = new_dim
        sf_x = H / h
        sf_y = W / w
        return BB(
            round(sf_x * self.x),
            round(sf_y * self.y),
            round(sf_x * self.X),
            round(sf_y * self.Y),
        )

    def relative(self, dim: Tuple[int, int]):
        h, w = dim
        return BB(self.x / w, self.y / h, self.X / w, self.Y / h)

    def absolute(self, dim: Tuple[int, int]):
        h, w = dim
        return BB(int(self.x * w), int(self.y * h), int(self.X * w), int(self.Y * h))

    def local_to(self, _bb):
        x, y, X, Y = self
        a, b, A, B = _bb
        return BB(x - a, y - b, X - a, Y - b)

    def jitter(self, noise, preserve_shape=True):
        if isinstance(noise, (int, float)):
            return BB([i + (noise - randint(2 * noise)) for i in self])
        elif isinstance(noise, (list, tuple)):
            if len(noise) == 2:
                dx, dy = noise
                dx, dy, dX, dY = dx / 2, dy / 2, dx / 2, dy / 2
            elif len(noise) == 4:
                dx, dy, dX, dY = noise
            if 0 < dx < 1:
                dx = int(self.w * dx)
            if 0 < dX < 1:
                dX = int(self.w * dX)
            if 0 < dy < 1:
                dy = int(self.h * dy)
            if 0 < dY < 1:
                dY = int(self.w * dY)
            dx = dx - 2 * randint(dx + 1)
            dy = dy - 2 * randint(dy + 1)
            if preserve_shape:
                dX = dx
                dY = dy
            else:
                dX = dX - 2 * randint(dX + 1)
                dY = dy - 2 * randint(dY + 1)
            dbb = BB(dx, dy, dX, dY)
            return BB([max(0, i + j) for i, j in zip(self, dbb)])

    def shrink_inplace(self):
        "return a new thing, shrunk"

    def add_padding(self, *pad):
        if len(pad) == 4:
            _x, _y, _X, _Y = pad
        else:
            (pad,) = pad
            _x, _y, _X, _Y = pad, pad, pad, pad
        x, y, X, Y = self.bb
        return max(0, x - _x), max(0, y - _y), X + _x, Y + _y

    def l2(self, other, xyfactor=(1, 1)):
        _x_, _y_ = xyfactor
        other = BB(other)
        xc, yc = self.xc, self.yc
        ac, bc = other.xc, other.yc
        return np.sqrt(_x_ * (xc - ac) ** 2 + _y_ * (yc - bc) ** 2)

    def distances(self, other_bbs, threshold=None, direction=None):
        other_bbs = bbfy(other_bbs)
        if direction:
            assert direction in "x,y,left,right,top,down".split(",")
            if direction == "x":
                output = [
                    (ix, bb, self.l2(bb, xyfactor=(1, 1000))) for (ix, bb) in other_bbs
                ]
                return pd.DataFrame(output, columns="ix,bb,dist".split(","))
            raise NotImplementedError("")
        return sorted(other_bbs, key=lambda obj: self.l2(obj[1]))

# %% ../nbs/bounding_boxes.ipynb 8
def df2bbs(df):
    """
    Convert a DataFrame to bounding boxes.

    Parameters:
    df (pd.DataFrame): The DataFrame to convert.

    Returns:
    list: A list of bounding boxes.
    """
    if "bb" in df.columns:
        try:
            return bbfy(df["bb"].values.tolist())
        except:
            return bbfy(df["bb"].map(lambda x: eval(x)).values.tolist())
    return [BB(bb) for bb in df[list("xyXY")].values.tolist()]


def bbs2df(bbs):
    """
    Convert bounding boxes to a DataFrame.

    Parameters:
    bbs (list): The bounding boxes to convert.

    Returns:
    pd.DataFrame: A DataFrame representing the bounding boxes.
    """
    bbs = [list(bb) for bb in bbs]
    return pd.DataFrame(bbs, columns=["x", "y", "X", "Y"])


def bbfy(bbs):
    """
    Convert bounding boxes to BB objects.

    Parameters:
    bbs (list): The bounding boxes to convert.

    Returns:
    list: A list of BB objects.
    """
    return [BB(bb) for bb in bbs]


def jitter(bbs, noise):
    """
    Add noise to bounding boxes. Useful when you have a lot of overlapping boxes.

    Parameters:
    bbs (list): The bounding boxes to add noise to.
    noise (float): The amount of noise to add.

    Returns:
    list: A list of bounding boxes with added noise.
    """
    return [BB(bb).jitter(noise) for bb in bbs]


def compute_eps(eps):
    """
    Compute epsilon values for bounding box manipulation.

    Parameters:
    eps (float or tuple): The epsilon value(s) to compute.

    Returns:
    tuple: A tuple of epsilon values.
    """
    if isinstance(eps, tuple):
        if len(eps) == 4:
            epsx, epsy, epsX, epsY = eps
        else:
            epsx, epsy = eps
            epsx, epsy, epsX, epsY = epsx / 2, epsy / 2, epsx / 2, epsy / 2
    else:
        epsx, epsy, epsX, epsY = eps / 2, eps / 2, eps / 2, eps / 2
    return epsx, epsy, epsX, epsY


def enlarge_bbs(bbs, eps=0.2):
    """
    Enlarge bounding boxes by a certain fraction.

    Parameters:
    bbs (list): The bounding boxes to enlarge.
    eps (float, optional): The fraction to enlarge by. Defaults to 0.2.

    Returns:
    list: A list of enlarged bounding boxes.
    """
    bbs = bbfy(bbs)
    epsx, epsy, epsX, epsY = compute_eps(eps)
    bbs = bbfy(bbs)
    shs = [(bb.h, bb.w) for bb in bbs]
    return [
        BB(x - (w * epsx), y - (h * epsy), X + (w * epsX), Y + (h * epsY))
        for (x, y, X, Y), (h, w) in zip(bbs, shs)
    ]


def shrink_bbs(bbs, eps=0.2):
    """
    Shrink bounding boxes by a certain fraction.

    Parameters:
    bbs (list): The bounding boxes to shrink.
    eps (float, optional): The fraction to shrink by. Defaults to 0.2.

    Returns:
    list: A list of shrunk bounding boxes.
    """
    bbs = bbfy(bbs)
    epsx, epsy, epsX, epsY = compute_eps(eps)
    bbs = bbfy(bbs)
    shs = [(bb.h, bb.w) for bb in bbs]
    return [
        BB(x + (w * epsx), y + (h * epsy), X - (w * epsX), Y - (h * epsY))
        for (x, y, X, Y), (h, w) in zip(bbs, shs)
    ]

# %% ../nbs/bounding_boxes.ipynb 9
def iou(bboxes1, bboxes2):
    """
    Calculates the Intersection over Union (IoU) between two sets of bounding boxes.

    Args:
        bboxes1 (list or numpy array): The first set of bounding boxes in the format [x, y, X, Y].
        bboxes2 (list or numpy array): The second set of bounding boxes in the format [x, y, X, Y].

    Returns:
        numpy array: The IoU between each pair of bounding boxes.

    """
    if isinstance(bboxes1, pd.DataFrame):
        bboxes1 = bboxes1[[*'xyXY']]
    if isinstance(bboxes2, pd.DataFrame):
        bboxes2 = bboxes2[[*'xyXY']]
    bboxes1 = np.array(bboxes1)
    bboxes2 = np.array(bboxes2)
    x11, y11, x12, y12 = np.split(bboxes1, 4, axis=1)
    x21, y21, x22, y22 = np.split(bboxes2, 4, axis=1)
    xA = np.maximum(x11, np.transpose(x21))
    yA = np.maximum(y11, np.transpose(y21))
    xB = np.minimum(x12, np.transpose(x22))
    yB = np.minimum(y12, np.transpose(y22))
    interArea = np.maximum((xB - xA), 0) * np.maximum((yB - yA), 0)
    boxAArea = (x12 - x11) * (y12 - y11)
    boxBArea = (x22 - x21) * (y22 - y21)
    iou = interArea / (boxAArea + np.transpose(boxBArea) - interArea)
    return iou


def compute_distance_matrix(bboxes1, bboxes2):
    """
    Compute the distance matrix between two sets of bounding boxes.

    Parameters:
    - bboxes1 (list): List of bounding boxes in the format [x, y, X, Y].
    - bboxes2 (list): List of bounding boxes in the format [x, y, X, Y].

    Returns:
    - distance_matrix (ndarray): 2D array containing the Euclidean distances between all pairs of bounding boxes.
    """

    # Convert the bounding box lists to NumPy arrays
    bboxes1 = np.array(bboxes1)
    bboxes2 = np.array(bboxes2)

    # Extract the x, y coordinates of the bounding boxes
    xy1 = bboxes1[:, :2]
    xy2 = bboxes2[:, :2]

    # Compute the squared Euclidean distances between all pairs of bounding box coordinates
    distance_matrix = np.sum((xy1[:, np.newaxis] - xy2) ** 2, axis=-1)

    # Take the square root to get the Euclidean distances
    distance_matrix = np.sqrt(distance_matrix)

    return distance_matrix


def compute_distances(df1, df2, shrink_factors=(1, 1)):
    """
    Compute the Euclidean distance matrix between bounding boxes in df1 and df2.

    Parameters:
    - df1 (DataFrame): The first DataFrame containing bounding boxes.
    - df2 (DataFrame): The second DataFrame containing bounding boxes.
    - shrink_factors (tuple, optional): The shrink factors to apply to the bounding boxes. Default is (1, 1).

    Returns:
    - distances (ndarray): The Euclidean distance matrix between the bounding boxes in df1 and df2.
    """
    sx, sy = shrink_factors
    bbs1 = np.array(df2bbs(df1)) / np.array([sx, sy, sx, sy])
    bbs2 = np.array(df2bbs(df2)) / np.array([sx, sy, sx, sy])

    distances = compute_distance_matrix(bbs1, bbs2)
    return distances

# %% ../nbs/bounding_boxes.ipynb 10
def split_bb_to_xyXY(df):
    """
    Convert the 'bb' column in the DataFrame to separate 'x', 'y', 'X', 'Y' columns.

    Args:
        df (pd.DataFrame): The DataFrame containing the bounding box information.

    Returns:
        pd.DataFrame: The DataFrame with separate 'x', 'y', 'X', 'Y' columns.

    Raises:
        AssertionError: If the input is not a DataFrame or if the 'bb' column is missing.
    """
    df = df.copy()
    assert isinstance(df, pd.DataFrame)
    if all([item in df.columns for item in "xyXY"]):
        return df
    assert "bb" in df.columns, "Expecting the df's bounding boxes to be in `bb` column"
    try:
        df["bb"] = df["bb"].map(eval)
    except:
        pass
    df["x"] = df["bb"].map(lambda x: x[0])
    df["y"] = df["bb"].map(lambda x: x[1])
    df["X"] = df["bb"].map(lambda x: x[2])
    df["Y"] = df["bb"].map(lambda x: x[3])
    df.drop(["bb"], axis=1, inplace=True)
    return df


def combine_xyXY_to_bb(df):
    """
    Combine `x`, `y`, `X`, `Y` columns into a single `bb` column.

    Args:
        df (pandas.DataFrame): The input DataFrame containing `x`, `y`, `X`, `Y` columns.

    Returns:
        pandas.DataFrame: The modified DataFrame with the `bb` column.

    Raises:
        AssertionError: If any of the columns `x`, `y`, `X`, `Y` are missing in the DataFrame.
    """
    df = df.copy()
    assert all(
        [item in df.columns for item in "xyXY"]
    ), "All the columns `x`, `y`, `X`, `Y` should be in df"
    df["bb"] = df[[*"xyXY"]].values.tolist()
    df.drop([*"xyXY"], inplace=True, axis=1)
    return df


def is_absolute(df):
    """
    Check if the bounding boxes in the given DataFrame are absolute.

    Args:
        df (pandas.DataFrame): The DataFrame containing bounding box coordinates.

    Returns:
        bool: True if the maximum value of the bounding box coordinates is greater than 1.1, False otherwise.
    """
    bbs = df2bbs(df)
    bbs = np.array(bbs)
    return bbs.max() > 1.1


def is_relative(df):
    """
    Check if the bounding box coordinates in the DataFrame are relative.

    Args:
        df (pandas.DataFrame): The DataFrame containing bounding box coordinates.

    Returns:
        bool: True if the bounding box coordinates are relative, False otherwise.
    """
    return not is_absolute(df)


def to_relative(df, height, width, force=False):
    """
    Converts bounding box coordinates in a DataFrame to relative coordinates.

    Args:
        df (pandas.DataFrame): The DataFrame containing bounding box coordinates.
        height (int): The height of the image.
        width (int): The width of the image.
        force (bool, optional): If True, forces conversion even if the coordinates are already relative.
                                Defaults to False.

    Returns:
        pandas.DataFrame: The DataFrame with bounding box coordinates converted to relative coordinates.
    """
    if not force and is_relative(df):
        return df
    df = df.copy()
    if "x" not in df.columns and "bb" in df.columns:
        _recombine = True
        df = split_bb_to_xyXY(df)
    else:
        _recombine = False
    df["x"] = df["x"] / width
    df["y"] = df["y"] / height
    df["X"] = df["X"] / width
    df["Y"] = df["Y"] / height
    if _recombine:
        df = combine_xyXY_to_bb(df)
    return df


def to_absolute(df, height, width, force=False):
    """
    Converts bounding box coordinates from relative to absolute values.

    Args:
        df (pandas.DataFrame): The DataFrame containing the bounding box coordinates.
        height (int): The height of the image.
        width (int): The width of the image.
        force (bool, optional): If True, forces the conversion even if the coordinates are already in absolute values. Defaults to False.

    Returns:
        pandas.DataFrame: The DataFrame with the bounding box coordinates converted to absolute values.
    """
    if not force and is_absolute(df):
        return df
    df = df.copy()
    if "x" not in df.columns and "bb" in df.columns:
        _recombine = True
        df = split_bb_to_xyXY(df)
    else:
        _recombine = False
    df["x"] = (np.clip(df["x"], 0, 1) * width).astype(np.uint16)
    df["y"] = (np.clip(df["y"], 0, 1) * height).astype(np.uint16)
    df["X"] = (np.clip(df["X"], 0, 1) * width).astype(np.uint16)
    df["Y"] = (np.clip(df["Y"], 0, 1) * height).astype(np.uint16)
    if _recombine:
        df = combine_xyXY_to_bb(df)
    return df

# %% ../nbs/bounding_boxes.ipynb 18
def merge_by_bb(df1, df2, suffixes=("_x", "_y"), iou_threshold=0.1):
    """Merge df1 columns to df2 by using iou
    Make sure both df1 & df2 are relative or both absolute
    """
    # df1, df2 = [df.copy().reset_index(drop=True) for df in [df1, df2]]
    assert all([c in df1.columns for c in "xyXY"])
    assert all([c in df2.columns for c in "xyXY"])
    ious = iou(df2bbs(df1), df2bbs(df2))
    _isin = isin(df2bbs(df1), df2bbs(df2), return_matrix=True)
    _isin_r = isin(df2bbs(df2), df2bbs(df1), return_matrix=True)
    (ixs, jxs) = np.nonzero(ious)
    ious = ious[ixs, jxs]
    _df1 = df1.iloc[ixs]
    _df1.columns = [f"{c}{suffixes[0]}" for c in df1.columns]
    _df2 = df2.iloc[jxs]
    _df2.columns = [f"{c}{suffixes[1]}" for c in df2.columns]
    output = pd.concat(
        [
            _df1.reset_index(names=f"index_{suffixes[0]}"),
            _df2.reset_index(names=f"index_{suffixes[1]}"),
        ],
        axis=1,
    )
    output["iou"] = ious
    output["isin"] = _isin[ixs, jxs]
    output["isin_r"] = _isin_r.T[ixs, jxs]
    output = output.query("iou > @iou_threshold")
    return output


def isin(bboxes1, bboxes2, return_matrix=True):
    """return indexes of those boxes from `bboxes1` that are completely inside `bboxes2`"""
    bboxes1 = np.array(bboxes1)
    bboxes2 = np.array(bboxes2)
    x11, y11, x12, y12 = np.split(bboxes1, 4, axis=1)
    x21, y21, x22, y22 = np.split(bboxes2, 4, axis=1)
    xA = np.maximum(x11, np.transpose(x21))
    yA = np.maximum(y11, np.transpose(y21))
    xB = np.minimum(x12, np.transpose(x22))
    yB = np.minimum(y12, np.transpose(y22))
    interArea = np.maximum((xB - xA), 0) * np.maximum((yB - yA), 0)
    boxAArea = (x12 - x11) * (y12 - y11)
    output = interArea / boxAArea
    if return_matrix:
        return output
    ixs = np.where(output == 1)[0]
    return ixs
