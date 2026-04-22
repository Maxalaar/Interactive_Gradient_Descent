from dash import Input, Output


def register_sync_loss_function_defaults(app, loss_functions: dict) -> None:
    """Sync X/Y range inputs whenever the selected loss function changes."""

    @app.callback(
        Output("x-min", "value"),
        Output("x-max", "value"),
        Output("y-min", "value"),
        Output("y-max", "value"),
        Input("loss-function-dropdown", "value"),
    )
    def sync_loss_function_defaults(loss_name: str):
        func = loss_functions[loss_name]
        lo, hi = func.get_parameter_range()
        return lo, hi, lo, hi
