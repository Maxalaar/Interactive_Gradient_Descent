from dash import ClientsideFunction, Input, Output

def register_cursor_management(app):
    app.clientside_callback(
        ClientsideFunction(
            namespace="cursor",
            function_name="update_cursor"
        ),
        Output("cursor-state", "data", allow_duplicate=True),
        Input("cursor-state", "data"),
        prevent_initial_call=True,
    )