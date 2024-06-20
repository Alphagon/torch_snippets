# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/imgaug_loader.ipynb.

# %% auto 0
__all__ = ['do', 'bw', 'rotate', 'pad', 'get_size', 'rescale', 'crop', 'imgaugbbs2bbs', 'bbs2imgaugbbs']

# %% ../nbs/imgaug_loader.ipynb 2
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from .loader import BB, PIL, bbs2df, df2bbs, np, pd, Image
from torch_snippets.bb_utils import (
    split_bb_to_xyXY,
    combine_xyXY_to_bb,
    to_relative,
    to_absolute,
)

# %% ../nbs/imgaug_loader.ipynb 3
def do(img, bbs=None, aug=None, cval=255):
    """
    Apply image augmentation to the input image and bounding boxes.

    Args:
        img (numpy.ndarray or PIL.Image.Image): The input image.
        bbs (pandas.DataFrame or None): The bounding boxes associated with the image.
        aug (imgaug.augmenters.Augmenter or None): The image augmentation object.
        cval (int): The constant value used for padding.

    Returns:
        tuple or PIL.Image.Image: If `bbs` is None, returns the augmented image.
        Otherwise, returns a tuple containing the augmented image and the augmented bounding boxes.
    """
    if isinstance(img, PIL.Image.Image):
        _Image = True
        img = np.array(img)
    else:
        _Image = False
    no_bbs = False
    if bbs is None:
        no_bbs = True
        bbs = []
    H, W = img.shape[:2]
    if isinstance(bbs, pd.DataFrame):
        _df = bbs.copy()
        _separate = True if "x" in _df.columns else False
        if not _separate:
            _df = split_bb_to_xyXY(_df)
        _relative = True if _df["x"].max() < 1 else False
        if _relative:
            _df = to_absolute(_df, H, W)
        bbs = df2bbs(_df)
        remaining_columns = [c for c in _df.columns if c not in "xyXY"]
        __df = _df[remaining_columns]
        _data_frame = True
    else:
        _data_frame = False

    bbs = bbs2imgaugbbs(bbs, img)
    img, bbs = aug(images=[img], bounding_boxes=[bbs])
    img, bbs = (img[0], imgaugbbs2bbs(bbs))
    H, W = img.shape[:2]

    if _Image:
        img = Image.fromarray(img)
    if _data_frame:
        _df = bbs2df(bbs)
        __df[[*"xyXY"]] = _df.values
        if _relative:
            __df = to_relative(__df, H, W)
        if not _separate:
            __df = combine_xyXY_to_bb(__df)
        bbs = __df
    if no_bbs:
        return img
    return img, bbs


def bw(img, bbs):
    """
    Applies grayscale augmentation to the input image.

    Args:
        img (numpy.ndarray): The input image.
        bbs (list): List of bounding boxes associated with the image.

    Returns:
        numpy.ndarray: The augmented image.

    """
    aug = iaa.Grayscale()
    return do(img, bbs, aug)


def rotate(img, bbs=None, angle=None, cval=255):
    """
    Rotate the input image and bounding boxes (if provided) by a given angle.

    Args:
        img (numpy.ndarray): The input image.
        bbs (list, optional): List of bounding boxes. Defaults to None.
        angle (float, optional): The angle of rotation in degrees. Defaults to None.
        cval (int, optional): The constant value used to fill the empty space after rotation. Defaults to 255.

    Returns:
        numpy.ndarray: The rotated image.
    """
    aug = iaa.Rotate(angle, cval=cval, fit_output=True)
    return do(img, bbs=bbs, aug=aug)


def pad(img, bbs, sz=None, deltas=None, cval=0):
    """
    Pad an image and its bounding boxes.

    Args:
        img (numpy.ndarray or PIL.Image.Image): The input image.
        bbs (list): List of bounding boxes.
        sz (tuple, optional): The desired size of the output image. If provided, the image will be padded to this size. Defaults to None.
        deltas (tuple, optional): The amount of padding to be applied on each side of the image. If provided, sz will be ignored. Defaults to None.
        cval (int, optional): The value used for padding. Defaults to 0.

    Returns:
        numpy.ndarray: The padded image.
    """
    if isinstance(img, np.ndarray):
        h, w = img.shape[:2]
    else:
        w, h = img.size
    if sz:
        H, W = sz
        deltas = (H - h) // 2, (W - w) // 2, (H - h) // 2, (W - w) // 2

    aug = iaa.Pad(deltas, pad_cval=cval)
    return do(img, bbs, aug)


def get_size(sz, h, w):
    """
    Calculate the target size (height and width) based on the input size and resize parameters.

    Args:
        sz (tuple, list, float, int): The resize parameters. It can be one of the following:
            - (tuple, list): A tuple or list containing a signal and target size (H, W).
                             The signal can be either 'at-least' or 'at-most'.
                             The target size represents the desired size of the image.
            - float: A float value representing the fraction of the input size.
            - int: An integer value representing the target size.
            - tuple: A tuple containing the target size (H, W).
                     The target size can be -1 to maintain the aspect ratio of the input size.
            - float: A float value representing the target size as a fraction of the input size.

        h (int): The height of the input size.
        w (int): The width of the input size.

    Returns:
        tuple: A tuple containing the target size (H, W).

    Raises:
        AssertionError: If the resize type is not 'at-least' or 'at-most'.

    """
    if isinstance(sz, (tuple, list)) and isinstance(sz[0], str):
        signal, (H, W) = sz
        assert signal in "at-least,at-most".split(
            ","
        ), "Resize type must be one of `at-least` or `at-most`"
        if signal == "at-least":
            f = max(H / h, W / w)
        if signal == "at-most":
            f = min(H / h, W / w)
        H, W = [i * f for i in [h, w]]
    elif isinstance(sz, float):
        frac = sz
        H, W = [i * frac for i in [h, w]]
    elif isinstance(sz, int):
        H, W = sz, sz
    elif isinstance(sz, tuple):
        H, W = sz
        if H == -1:
            _, W = sz
            f = W / w
            H = f * h
        elif W == -1:
            H, _ = sz
            f = H / h
            W = f * w
        elif isinstance(H, float):
            H = H * h
        elif isinstance(W, float):
            W = W * h
    H, W = int(H), int(W)
    return H, W


def rescale(im, bbs, sz):
    """
    Rescales the input image and bounding boxes to the specified size.

    Args:
        im (PIL.Image.Image or numpy.ndarray): The input image.
        bbs (list): List of bounding boxes.
        sz (tuple): The target size (height, width) to resize the image.

    Returns:
        PIL.Image.Image: The resized image.
        list: The resized bounding boxes.

    """
    if isinstance(im, PIL.Image.Image):
        to_pil = True
        im = np.array(im)
    else:
        to_pil = False
    h, w = im.shape[:2]
    H, W = get_size(sz, h, w)
    aug = iaa.Resize({"height": H, "width": W})
    im, bbs = do(im, bbs, aug)
    if to_pil:
        im = PIL.Image.fromarray(im)
    return im, bbs


def crop(img, bbs, deltas):
    """
    Crop the image and bounding boxes using the specified deltas.

    Args:
        img (numpy.ndarray): The input image.
        bbs (list): List of bounding boxes.
        deltas (tuple or list): The crop deltas in the form of (top, right, bottom, left).

    Returns:
        numpy.ndarray: The cropped image.
        list: The cropped bounding boxes.
    """
    aug = iaa.Crop(deltas)
    return do(img, bbs, aug)


def imgaugbbs2bbs(bbs):
    """
    Converts a list of imgaug bounding boxes to a list of custom BB objects.

    Args:
        bbs (list): A list of imgaug bounding boxes.

    Returns:
        list: A list of custom BB objects.

    """
    if bbs is None:
        return None
    return [
        BB([int(i) for i in (bb.x1, bb.y1, bb.x2, bb.y2)])
        for bb in bbs[0].bounding_boxes
    ]


def bbs2imgaugbbs(bbs, img):
    """
    Convert a list of bounding boxes to an imgaug BoundingBoxesOnImage object.

    Args:
        bbs (list): List of bounding boxes in the format [(x1, y1, x2, y2), ...].
        img (numpy.ndarray): Input image.

    Returns:
        imgaug.BoundingBoxesOnImage: BoundingBoxesOnImage object representing the bounding boxes on the image.
    """
    if bbs is None:
        return None
    return BoundingBoxesOnImage(
        [BoundingBox(x1=x, y1=y, x2=X, y2=Y) for x, y, X, Y in bbs], shape=img.shape
    )
