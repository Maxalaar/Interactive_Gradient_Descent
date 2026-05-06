import json
import dash
from dash import Input, Output, State, html, dcc, callback_context
from dash.exceptions import PreventUpdate

def register_optimizer_management(app, optimizers: dict) -> None:
    """Génère dynamiquement les champs pour les hyperparamètres de l'optimiseur."""

    @app.callback(
        Output("optimizer-params-container", "children"),
        Output("optimizer-hyperparams", "data"),
        Output("iterations", "value"),
        Input("optimizer-name", "value"),
    )
    def update_optimizer_ui(optimizer_name: str):
        optimizer = optimizers[optimizer_name]
        defaults = optimizer.get_hyperparameter_defaults()
        children = []
        for name, default_value in defaults.items():
            label = name.replace('_', ' ').capitalize()
            children.append(html.Div([
                html.Label(label, style={"fontWeight": "bold"}),
                dcc.Input(
                    id={"type": "optimizer-param", "index": name},
                    # type="number",
                    value=default_value,
                    step="any",
                    style={"width": "100%", "marginBottom": "10px"}
                )
            ]))
        return children, defaults, optimizer.get_default_iterations()

    @app.callback(
        Output("optimizer-hyperparams", "data", allow_duplicate=True),
        Input({"type": "optimizer-param", "index": dash.dependencies.ALL}, "value"),
        State("optimizer-hyperparams", "data"),
        prevent_initial_call=True,
    )
    def update_hyperparams_from_input(values, current_data):
        if not current_data:
            raise PreventUpdate
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        trigger = ctx.triggered[0]
        try:
            trigger_id = json.loads(trigger["prop_id"].split(".")[0])
            param_name = trigger_id["index"]
            new_value = trigger["value"]
        except (json.JSONDecodeError, KeyError, IndexError):
            raise PreventUpdate

        if new_value is None:
            raise PreventUpdate

        current_data[param_name] = float(new_value)
        return current_data