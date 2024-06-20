# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/bokeh_plotting.ipynb.

# %% auto 0
__all__ = ['parse_sz', 'get_bplot']

# %% ../nbs/bokeh_plotting.ipynb 2
from bokeh.io import output_notebook, show as bshow
from bokeh.plotting import figure, from_networkx
from bokeh.models import (
    Circle,
    Rect,
    WheelZoomTool,
    PanTool,
    BoxZoomTool,
    ResetTool,
    MultiLine,
    NodesAndLinkedEdges,
    EdgesAndLinkedNodes,
    HoverTool,
    TapTool,
    BoxSelectTool,
)
from bokeh.palettes import Spectral7
import numpy as np

# %% ../nbs/bokeh_plotting.ipynb 3
def parse_sz(size):
    """
    Parses the size argument and returns a tuple of width and height.

    Args:
        size (int or tuple): The size argument to be parsed.

    Returns:
        tuple: A tuple of width and height.

    Raises:
        NotImplementedError: If the size argument is not an int or a tuple of length 2.
    """
    if isinstance(size, int):
        return size, size
    elif isinstance(size, tuple):
        if len(size) == 2:
            return size
    raise NotImplementedError(f"function is not implemented for {size}")


def get_bplot(sz=500, **kwargs):
    """
    Create a Bokeh plot with specified size and tools.

    Parameters:
    - sz (int): Size of the plot in pixels.
    - **kwargs: Additional keyword arguments for customizing the plot.

    Returns:
    - plot (bokeh.plotting.Figure): Bokeh plot object.

    """
    h, w = parse_sz(sz)
    output_notebook()
    plot = figure(
        tools=[WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool()],
        plot_width=w,
        plot_height=h,
        match_aspect=kwargs.pop("match_aspect", False),
    )
    plot.add_tools(
        HoverTool(
            tooltips=[("index", "$index")]
            + [(i, f"@{i}") for i in kwargs.get("tooltips", [])]
        ),
        TapTool(),
        BoxSelectTool(),
    )

    plot.toolbar.active_scroll = plot.select_one(WheelZoomTool)
    plot.toolbar.active_drag = plot.select_one(PanTool)
    return plot
