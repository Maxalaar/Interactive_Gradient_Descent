import numpy as np

from build_surface import build_surface
from compute_loss_landscape import compute_loss_landscape
from constants import LANDSCAPE_SHOW, LOSS_LANDSCAPE_TRACE_NAME
from loss_function import LossFunction


def create_loss_landscape_figure(
    loss_function: LossFunction,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    sample_number: int,
    toggle_value: list,
) -> dict:
    """
    Build the Plotly loss-landscape figure and return it as a plain dict
    suitable for use as a Dash ``dcc.Graph`` figure.

    Args:
        loss_function:  LossFunction instance to visualise.
        x_min, x_max:   Bounds for the X axis.
        y_min, y_max:   Bounds for the Y axis.
        sample_number:  Grid resolution (points per axis).
        toggle_value:   List that contains ``LANDSCAPE_SHOW`` when the surface
                        should be visible, empty list otherwise.

    Returns:
        Plotly figure serialised as a ``dict``.
    """
    default_range = loss_function.get_parameter_range()
    if x_min is None or x_max is None or x_min >= x_max:
        x_min, x_max = default_range
    if y_min is None or y_max is None or y_min >= y_max:
        y_min, y_max = default_range

    X, Y, Z = compute_loss_landscape(
        loss_function,
        sample_number,
        x_range=[x_min, x_max],
        y_range=[y_min, y_max],
    )

    figure = build_surface(X, Y, Z).to_dict()

    figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
    figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]

    z_min, z_max = float(Z.min()), float(Z.max())
    padding = (z_max - z_min) * 0.05
    figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

    visible = LANDSCAPE_SHOW in (toggle_value or [])
    for trace in figure["data"]:
        if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
            trace["visible"] = visible
            break

    return figure
