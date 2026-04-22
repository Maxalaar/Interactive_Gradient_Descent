import uuid
import time
from typing import Optional

from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from compute_optimization_path import compute_optimization_path
from constants import DEFAULT_PATH_COLOR


def register_on_click(app, loss_functions: dict, optimizers: dict) -> None:

    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Output("last-click-time", "data", allow_duplicate=True),
        Output("path-counter-store", "data", allow_duplicate=True),
        Input("surface", "clickData"),
        State("loss-name", "data"),
        State("optimizer-name", "value"),
        State("learning-rate", "value"),
        State("iterations", "value"),
        State("paths-store", "data"),
        State("last-click-time", "data"),
        State("path-counter-store", "data"),
        prevent_initial_call=True,
    )
    def on_click(
        clickData,
        loss_name: Optional[str],
        optimizer_name: str,
        learning_rate,
        iterations,
        current_paths,
        last_click_time,
        path_counter,
    ):
        if clickData is None or loss_name is None:
            raise PreventUpdate

        now = time.time()
        if now - last_click_time < 0.25:
            raise PreventUpdate

        loss_function = loss_functions[loss_name]
        optimizer = optimizers[optimizer_name]

        x0 = clickData["points"][0]["x"]
        y0 = clickData["points"][0]["y"]

        if not isinstance(learning_rate, (int, float)) or learning_rate <= 0:
            learning_rate = optimizer.get_default_lr()
        else:
            learning_rate = float(learning_rate)

        if iterations is None or iterations < 1:
            iterations = optimizer.get_default_iterations()
        else:
            iterations = int(iterations)

        path = compute_optimization_path(
            loss_function,
            start_parameters=[x0, y0],
            optimizer=optimizer,
            learning_rate=learning_rate,
            iteration_number=iterations,
        )

        new_counter = (path_counter or 0) + 1
        new_path = {
            "id": str(uuid.uuid4()),
            "name": f"Path {new_counter}",
            "color": DEFAULT_PATH_COLOR,
            "visible": True,
            "data": {
                "x": path[:, 0].tolist(),
                "y": path[:, 1].tolist(),
                "z": path[:, 2].tolist(),
            },
        }

        updated_paths = list(current_paths or []) + [new_path]
        return updated_paths, now, new_counter
