from typing import List

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
    toggle_value: List[str],
) -> dict:
    default_range = loss_function.get_parameter_range()
    x_min, x_max = (x_min, x_max) if (x_min is not None and x_max is not None and x_min < x_max) else default_range
    y_min, y_max = (y_min, y_max) if (y_min is not None and y_max is not None and y_min < y_max) else default_range

    X, Y, Z = compute_loss_landscape(loss_function, sample_number, [x_min, x_max], [y_min, y_max])
    figure = build_surface(X, Y, Z).to_dict()

    z_min, z_max = float(Z.min()), float(Z.max())
    padding = (z_max - z_min) * 0.05

    figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
    figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
    figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

    visible = LANDSCAPE_SHOW in (toggle_value or [])
    for trace in figure["data"]:
        if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
            trace["visible"] = visible
            break

    return figure