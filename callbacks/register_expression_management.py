from dash import Input, Output
from dash.exceptions import PreventUpdate

def register_expression_management(app, loss_functions: dict) -> None:
    @app.callback(
        Output("function-expression", "value"),
        Input("loss-function-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_textarea_from_dropdown(selected_func):
        if selected_func is None:
            raise PreventUpdate
        return loss_functions[selected_func].get_expression()