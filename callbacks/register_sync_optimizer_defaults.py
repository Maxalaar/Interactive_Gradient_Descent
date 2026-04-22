from dash import Input, Output


def register_sync_optimizer_defaults(app, optimizers: dict) -> None:
    """Sync learning-rate and iteration inputs when the optimizer selection changes."""

    @app.callback(
        Output("learning-rate", "value"),
        Output("iterations", "value"),
        Input("optimizer-name", "value"),
    )
    def sync_optimizer_defaults(optimizer_name: str):
        optimizer = optimizers[optimizer_name]
        return optimizer.get_default_lr(), optimizer.get_default_iterations()
