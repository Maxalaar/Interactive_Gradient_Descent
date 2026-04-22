import numpy as np
import plotly.graph_objects as go

from constants import LOSS_LANDSCAPE_TRACE_NAME


def build_surface(X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> go.Figure:
    """
    Build the base Plotly 3-D surface figure for the loss landscape.

    Args:
        X, Y, Z:  Meshgrid arrays returned by ``compute_loss_landscape``.

    Returns:
        A ``go.Figure`` ready to be serialised with ``.to_dict()``.
    """
    figure = go.Figure()

    figure.add_trace(go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale="RdBu",
        opacity=0.9,
        showscale=False,
        name=LOSS_LANDSCAPE_TRACE_NAME,
    ))

    figure.update_layout(
        scene=dict(
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
            aspectmode="cube",          # prevents Z from dominating on flat functions
            uirevision="keep",
            xaxis_title="Parameter 1",
            yaxis_title="Parameter 2",
            zaxis_title="Loss",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision="keep",
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor="#cccccc",
            borderwidth=1,
        ),
        showlegend=False,
    )

    return figure
