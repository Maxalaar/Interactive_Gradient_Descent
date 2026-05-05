import random
import uuid
from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from compute_optimization_path import compute_optimization_path


def register_random_start(app, loss_functions, optimizers):
    @app.callback(
        output=[
            Output("paths-store", "data", allow_duplicate=True),
            Output("path-counter-store", "data", allow_duplicate=True),
        ],
        inputs=[Input("random-start-button", "n_clicks")],
        state=[
            State("surface", "figure"),
            State("loss-name", "data"),
            State("optimizer-name", "value"),
            State("learning-rate", "value"),
            State("iterations", "value"),
            State("paths-store", "data"),
            State("path-counter-store", "data"),
            State("x-min", "value"),
            State("x-max", "value"),
            State("y-min", "value"),
            State("y-max", "value"),
        ],
        running=[(Output("cursor-state", "data"), "busy", "idle")],
        prevent_initial_call=True,
    )
    def random_start_callback(
        n_clicks,
        figure,
        loss_name,
        optimizer_name,
        learning_rate,
        iterations,
        current_paths,
        path_counter,
        x_min_input,
        x_max_input,
        y_min_input,
        y_max_input,
    ):
        if not n_clicks or loss_name is None:
            raise PreventUpdate

        # 1. Récupérer la zone affichée (axes X et Y)
        # On tente de lire les ranges depuis la figure (zoom utilisateur)
        if figure and "layout" in figure and "scene" in figure["layout"]:
            x_axis = figure["layout"]["scene"].get("xaxis", {})
            y_axis = figure["layout"]["scene"].get("yaxis", {})
            x_range = x_axis.get("range")
            y_range = y_axis.get("range")
        else:
            x_range = y_range = None

        # Fallback sur les valeurs des champs input si les ranges ne sont pas définis
        if not x_range or len(x_range) != 2:
            x_min = x_min_input if x_min_input is not None else -5.0
            x_max = x_max_input if x_max_input is not None else 5.0
            x_range = (x_min, x_max)
        if not y_range or len(y_range) != 2:
            y_min = y_min_input if y_min_input is not None else -5.0
            y_max = y_max_input if y_max_input is not None else 5.0
            y_range = (y_min, y_max)

        # 2. Générer un point aléatoire uniforme dans le rectangle
        x0 = random.uniform(x_range[0], x_range[1])
        y0 = random.uniform(y_range[0], y_range[1])

        # 3. Paramètres d'optimisation
        loss_function = loss_functions[loss_name]
        optimizer = optimizers[optimizer_name]

        if not isinstance(learning_rate, (int, float)) or learning_rate <= 0:
            learning_rate = optimizer.get_default_lr()
        else:
            learning_rate = float(learning_rate)

        if iterations is None or iterations < 1:
            iterations = optimizer.get_default_iterations()
        else:
            iterations = int(iterations)

        # 4. Calcul de la trajectoire
        path = compute_optimization_path(
            loss_function,
            start_parameters=[x0, y0],
            optimizer=optimizer,
            learning_rate=learning_rate,
            iteration_number=iterations,
        )

        # 5. Créer l'entrée du chemin
        def random_color():
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            return f"#{r:02x}{g:02x}{b:02x}"

        new_counter = (path_counter or 0) + 1
        new_path = {
            "id": str(uuid.uuid4()),
            "name": f"Random start {new_counter}",
            "color": random_color(),
            "visible": True,
            "data": {
                "x": path[:, 0].tolist(),
                "y": path[:, 1].tolist(),
                "z": path[:, 2].tolist(),
            },
        }

        updated_paths = list(current_paths or []) + [new_path]
        return updated_paths, new_counter