import copy
from dash import Input, Output, State, no_update, callback_context
from dash.exceptions import PreventUpdate

from build_surface import build_surface
from compute_loss_landscape import compute_loss_landscape
from constants import LANDSCAPE_SHOW, LOSS_LANDSCAPE_TRACE_NAME
from preserve_camera_state import preserve_camera_state


def register_update_loss_landscape(app, loss_functions: dict, default_sample_number: int) -> None:
    @app.callback(
        output=[
            Output("surface", "figure", allow_duplicate=True),
            Output("paths-store", "data", allow_duplicate=True),
            Output("loss-name", "data"),
            Output("path-counter-store", "data", allow_duplicate=True),
        ],
        inputs=[
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
        ],
        running=[(Output("cursor-state", "data"), "busy", "idle")],
        background=True,
        prevent_initial_call=True,
    )
    def update_landscape(
            n_clicks, loss_name, x_min, x_max, y_min, y_max,
            sample_number, toggle_value, current_figure, current_paths, stored_loss_name,
    ):
        if loss_name is None:
            raise PreventUpdate

        loss_func = loss_functions[loss_name]
        sample_number = sample_number or default_sample_number
        default_range = loss_func.get_parameter_range()

        x_min, x_max = (x_min, x_max) if (x_min is not None and x_max is not None and x_min < x_max) else default_range
        y_min, y_max = (y_min, y_max) if (y_min is not None and y_max is not None and y_min < y_max) else default_range

        X, Y, Z = compute_loss_landscape(loss_func, sample_number, [x_min, x_max], [y_min, y_max])
        z_min, z_max = float(Z.min()), float(Z.max())
        padding = (z_max - z_min) * 0.05

        # Same function: update in-place, keep paths & camera
        if current_figure is not None and stored_loss_name == loss_name:
            updated_figure = copy.deepcopy(current_figure)
            preserve_camera_state(updated_figure, callback_context.inputs.get("surface.relayoutData"))

            for trace in updated_figure["data"]:
                if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                    trace.update(x=X, y=Y, z=Z, visible=LANDSCAPE_SHOW in (toggle_value or []))
                    break

            updated_figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
            updated_figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
            updated_figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]
            return updated_figure, no_update, stored_loss_name, no_update

        # New function: rebuild, clear paths
        figure = build_surface(X, Y, Z).to_dict()
        preserve_camera_state(figure, callback_context.inputs.get("surface.relayoutData"))

        figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
        figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
        figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

        for trace in figure["data"]:
            if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                trace["visible"] = True
                break

        return figure, [], loss_name, 0