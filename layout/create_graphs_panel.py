from dash import dcc, html

def create_graphs_panel(loss_landscape_surface):
    return html.Div([
        dcc.Graph(
            id="surface",
            figure=loss_landscape_surface,
            style={'height': '100%', 'width': '100%'},
            config={'responsive': True}
        ),
    ], style={
        'flex': '1',
        'padding': '10px',
        'display': 'flex',
        'flexDirection': 'column',
        'minHeight': 0,
        'height': '100%',    # Force la hauteur à 100% du parent
    })