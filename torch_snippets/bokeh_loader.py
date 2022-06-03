# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/bokeh_plotting.ipynb (unless otherwise specified).

__all__ = ['parse_sz', 'get_bplot']

# Cell
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


def parse_sz(size):
    if isinstance(size, int):
        return size, size
    elif isinstance(size, tuple):
        if len(size) == 2:
            return size
    raise NotImplementedError(f"function is not implemented for {size}")


def get_bplot(sz=500, **kwargs):
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