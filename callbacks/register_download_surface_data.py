from dash import Input, Output, State
from dash.exceptions import PreventUpdate


def register_download_surface_data(app, loss_functions):
    @app.callback(
        Output("download-surface-txt", "data"),
        Input("download-surface-button", "n_clicks"),
        State("loss-name", "data"),
        State("x-min", "value"),
        State("x-max", "value"),
        State("y-min", "value"),
        State("y-max", "value"),
        State("sample-number", "value"),
        prevent_initial_call=True,
    )
    def generate_surface_data(n_clicks, loss_name, x_min, x_max, y_min, y_max, sample_number):
        if not n_clicks or loss_name is None:
            raise PreventUpdate

        loss_func = loss_functions[loss_name]
        default_range = loss_func.get_parameter_range()
        x_min, x_max = (
            (x_min, x_max) if (x_min is not None and x_max is not None and x_min < x_max) else default_range
        )
        y_min, y_max = (
            (y_min, y_max) if (y_min is not None and y_max is not None and y_min < y_max) else default_range
        )
        sample_number = sample_number or 100

        from compute_loss_landscape import compute_loss_landscape
        X, Y, Z = compute_loss_landscape(loss_func, sample_number, [x_min, x_max], [y_min, y_max])

        lines = []
        ny, nx = Z.shape
        for i in range(ny):          # iterate over y (rows of the grid)
            for j in range(nx):      # iterate over x (columns)
                lines.append(f"{X[i, j]:.10g} {Y[i, j]:.10g} {Z[i, j]:.10g}")
            lines.append("")         # blank line between y‑blocks
        text = "\n".join(lines)

        import base64
        content_b64 = base64.b64encode(text.encode()).decode()
        return {"content": content_b64, "filename": "surface_data.txt", "base64": True}