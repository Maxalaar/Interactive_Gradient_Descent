from dash import Input, Output

from constants import LANDSCAPE_SHOW


def register_toggle_loss_landscape_visibility(app) -> None:
    @app.callback(
        Output("landscape-visible-store", "data"),
        Input("show-loss-landscape-toggle", "value"),
    )
    def toggle_landscape_visibility(toggle_value):
        return LANDSCAPE_SHOW if toggle_value and LANDSCAPE_SHOW in toggle_value else ""
