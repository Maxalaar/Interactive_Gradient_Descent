import copy

from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate

from build_surface import build_surface
from compute_loss_landscape import compute_loss_landscape
from constants import LANDSCAPE_SHOW, LOSS_LANDSCAPE_TRACE_NAME


def register_update_loss_landscape(app, loss_functions: dict, default_sample_number: int) -> None:
    @app.callback(
        Output("surface", "figure", allow_duplicate=True),
        Output("paths-store", "data", allow_duplicate=True),
        Output("loss-name", "data"),
        Input("update-loss-landscape-button", "n_clicks"),
        State("loss-function-dropdown", "value"),
        State("x-min", "value"),
        State("x-max", "value"),
        State("y-min", "value"),
        State("y-max", "value"),
        State("sample-number", "value"),
        State("show-loss-landscape-toggle", "value"),
        State("surface", "figure"),
        State("paths-store", "data"),
        State("loss-name", "data"),
        prevent_initial_call=True,
    )
    def update_landscape(
        n_clicks,
        loss_name,
        x_min, x_max,
        y_min, y_max,
        sample_number,
        toggle_value,
        current_figure,
        current_paths,
        stored_loss_name,
    ):
        if loss_name is None:
            raise PreventUpdate

        loss_function = loss_functions[loss_name]
        if sample_number is None:
            sample_number = default_sample_number

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

        z_min, z_max = float(Z.min()), float(Z.max())
        padding = (z_max - z_min) * 0.05

        # ------------------------------------------------------------------
        # Same loss function — update the surface data in-place so the camera
        # position and existing paths are preserved.
        # ------------------------------------------------------------------
        if current_figure is not None and stored_loss_name == loss_name:
            updated_figure = copy.deepcopy(current_figure)

            for trace in updated_figure["data"]:
                if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                    trace["x"] = X
                    trace["y"] = Y
                    trace["z"] = Z
                    trace["visible"] = LANDSCAPE_SHOW in (toggle_value or [])
                    break

            updated_figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
            updated_figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
            updated_figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

            return updated_figure, no_update, stored_loss_name

        # ------------------------------------------------------------------
        # Loss function changed — rebuild from scratch and clear paths.
        # ------------------------------------------------------------------
        figure = build_surface(X, Y, Z).to_dict()
        figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
        figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
        figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

        for trace in figure["data"]:
            if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                trace["visible"] = True
                break

        return figure, [], loss_name
