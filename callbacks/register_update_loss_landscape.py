import copy
from dash import Input, Output, State, no_update, callback_context
from dash.exceptions import PreventUpdate

from build_surface import build_surface
from compute_loss_landscape import compute_loss_landscape
from constants import LANDSCAPE_SHOW, LOSS_LANDSCAPE_TRACE_NAME
from preserve_camera_state import preserve_camera_state

_STATUS_BASE = {
    "padding": "5px 8px", "borderRadius": "4px",
    "fontSize": "11px", "lineHeight": "1.4", "marginTop": "4px",
}
_STATUS_ERROR   = {**_STATUS_BASE, "backgroundColor": "#f8d7da", "color": "#721c24"}
_STATUS_HIDDEN  = {"display": "none"}
_STATUS_SUCCESS = {**_STATUS_BASE, "backgroundColor": "#d4edda", "color": "#155724"}


def register_update_loss_landscape(app, loss_functions: dict, default_sample_number: int) -> None:
    @app.callback(
        output=[
            Output("surface", "figure", allow_duplicate=True),
            Output("paths-store", "data", allow_duplicate=True),
            Output("loss-name", "data"),
            Output("path-counter-store", "data", allow_duplicate=True),
            Output("custom-loss-status", "children", allow_duplicate=True),
            Output("custom-loss-status", "style", allow_duplicate=True),
            Output("loss-function-dropdown", "value", allow_duplicate=True),
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
            State("function-expression", "value"),
        ],
        running=[(Output("cursor-state", "data"), "busy", "idle")],
        prevent_initial_call=True,
    )
    def update_landscape(
            n_clicks, selected_loss_name, x_min, x_max, y_min, y_max,
            sample_number, toggle_value, current_figure, current_paths,
            stored_loss_name, expression_in_editor,
    ):
        if selected_loss_name is None:
            raise PreventUpdate

        # 1. Determine if the expression has been edited
        raw_expr = (expression_in_editor or "").strip()
        selected_func = loss_functions[selected_loss_name]
        original_expr = selected_func.get_expression()
        expression_changed = (raw_expr != original_expr)

        target_loss_name = selected_loss_name
        custom_func = loss_functions["Custom"]
        dropdown_update = no_update
        status_msg = ""
        status_style = _STATUS_HIDDEN

        if expression_changed:
            # Validate the edited expression
            error = custom_func.validate(raw_expr)
            if error:
                return (
                    no_update, no_update, no_update, no_update,
                    f"✖ {error}", _STATUS_ERROR, no_update,
                )
            # Apply the new expression to the custom function (silent success)
            custom_func.set_expression(raw_expr)
            target_loss_name = "Custom"
            dropdown_update = "Custom"
            # No success message – the div remains hidden

        # 2. Use the determined loss function
        loss_func = loss_functions[target_loss_name]
        sample_number = sample_number or default_sample_number
        default_range = loss_func.get_parameter_range()

        x_min, x_max = (
            (x_min, x_max)
            if (x_min is not None and x_max is not None and x_min < x_max)
            else default_range
        )
        y_min, y_max = (
            (y_min, y_max)
            if (y_min is not None and y_max is not None and y_min < y_max)
            else default_range
        )

        # Compute landscape
        X, Y, Z = compute_loss_landscape(loss_func, sample_number, [x_min, x_max], [y_min, y_max])
        z_min, z_max = float(Z.min()), float(Z.max())
        padding = (z_max - z_min) * 0.05

        # 3. Decide whether we can update in-place or must rebuild (clearing paths)
        # Rebuild if: function name changed OR expression changed (even if name same)
        must_rebuild = (stored_loss_name != target_loss_name) or expression_changed

        if not must_rebuild and current_figure is not None:
            # Same function, no change in expression → update trace in-place, keep paths
            updated_figure = copy.deepcopy(current_figure)
            preserve_camera_state(updated_figure, callback_context.inputs.get("surface.relayoutData"))

            for trace in updated_figure["data"]:
                if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                    trace.update(x=X, y=Y, z=Z, visible=LANDSCAPE_SHOW in (toggle_value or []))
                    break

            updated_figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
            updated_figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
            updated_figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

            return (
                updated_figure,
                no_update,      # keep existing paths
                target_loss_name,
                no_update,      # keep path counter
                status_msg,
                status_style,
                dropdown_update,
            )
        else:
            # Rebuild figure and clear all paths
            figure = build_surface(X, Y, Z).to_dict()
            preserve_camera_state(figure, callback_context.inputs.get("surface.relayoutData"))

            figure["layout"]["scene"]["xaxis"]["range"] = [x_min, x_max]
            figure["layout"]["scene"]["yaxis"]["range"] = [y_min, y_max]
            figure["layout"]["scene"]["zaxis"]["range"] = [z_min - padding, z_max + padding]

            for trace in figure["data"]:
                if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                    trace["visible"] = True
                    break

            return (
                figure,
                [],                     # clear paths
                target_loss_name,
                0,                      # reset path counter
                status_msg,
                status_style,
                dropdown_update,
            )