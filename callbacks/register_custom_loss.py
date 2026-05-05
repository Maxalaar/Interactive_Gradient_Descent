from dash import Input, Output


def register_custom_loss(app, loss_functions: dict) -> None:
    """Toggle the custom expression editor based on the selected loss function."""

    @app.callback(
        Output("custom-loss-editor", "style"),
        Input("loss-function-dropdown", "value"),
    )
    def toggle_custom_editor(loss_name: str) -> dict:
        visible = loss_name == "Custom"
        return {"display": "block" if visible else "none", "marginBottom": "10px"}