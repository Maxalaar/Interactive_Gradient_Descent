from dash import Input, Output, State

from constants import LANDSCAPE_SHOW


def register_toggle_loss_landscape_visibility(app) -> None:
    @app.callback(
        Output("surface", "figure", allow_duplicate=True),
        Output("landscape-visible-store", "data"),
        Input("show-loss-landscape-toggle", "value"),
        State("surface", "figure"),
        State("surface", "relayoutData"),
        prevent_initial_call='initial_duplicate',
    )
    def toggle_landscape_visibility(toggle_value, figure, relayoutData):
        if relayoutData and "scene.camera" in relayoutData:
            figure["layout"]["scene"]["camera"] = relayoutData["scene.camera"]

        landscape_visible_store = LANDSCAPE_SHOW if toggle_value and LANDSCAPE_SHOW in toggle_value else ""

        return figure, landscape_visible_store