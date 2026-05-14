from dash import dcc, html

def create_paths_panel() -> html.Div:
    """Panneau latéral dédié à l'affichage et à la gestion des chemins d'optimisation."""
    return html.Div([
        html.H4("Optimization Paths", style={"marginTop": "10px", "marginBottom": "5px"}),

        html.Button(
            "Random Start",
            id="random-start-button",
            n_clicks=0,
            style={
                "backgroundColor": "#28a745", "color": "white",
                "border": "none", "padding": "4px 8px",
                "borderRadius": "4px", "cursor": "pointer",
                "fontSize": "12px", "width": "100%", "marginTop": "5px",
            },
        ),

        html.Button(
            "Clear All Paths",
            id="clear-paths-button",
            n_clicks=0,
            style={
                "backgroundColor": "#dc3545", "color": "white",
                "border": "none", "padding": "4px 8px",
                "borderRadius": "4px", "cursor": "pointer",
                "fontSize": "12px", "width": "100%", "marginTop": "10px",
                "marginBottom": "5px",
            },
        ),

        html.Div(id="paths-list", children=[]),

        # Stores dédiés aux chemins
        dcc.Store(id="paths-store", data=[]),
        dcc.Store(id="last-click-time", data=0),
        dcc.Store(id="path-counter-store", data=0),
        dcc.Store(id="cursor-state", data="idle"),

        dcc.Download(id="download-path-txt"),
    ], style={
        "flex": "0 0 280px",
        "padding": "10px",
        "marginRight": "10px",
        "overflowY": "auto",
        "backgroundColor": "#f8f9fa",
        "borderRadius": "8px",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
    })