from dash import dcc, html

from constants import (
    LANDSCAPE_SHOW,
    LANDSCAPE_VISIBLE_STORE_ID,
    LOSS_NAME_STORE_ID,
    PATHS_STORE_ID,
)


def create_options_panel(
    loss_functions: dict,
    optimizers: dict,
    default_sample_number: int,
    first_function_name: str,
    default_range: list,
    first_optimizer_name: str,
    first_optimizer,
) -> html.Div:

    return html.Div([

        # ── Loss landscape ──────────────────────────────────────────────
        html.Div([
            html.Label("Loss Function:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="loss-function-dropdown",
                options=[{"label": n, "value": n} for n in loss_functions],
                value=first_function_name,
                clearable=False,
                style={"marginBottom": "15px"},
            ),

            html.Label("X Range:", style={"fontWeight": "bold"}),
            html.Div([
                dcc.Input(id="x-min", type="number", value=default_range[0],
                          style={"width": "80px", "marginRight": "5px"}),
                html.Span(" to "),
                dcc.Input(id="x-max", type="number", value=default_range[1],
                          style={"width": "80px", "marginLeft": "5px"}),
            ], style={"marginBottom": "10px"}),

            html.Label("Y Range:", style={"fontWeight": "bold"}),
            html.Div([
                dcc.Input(id="y-min", type="number", value=default_range[0],
                          style={"width": "80px", "marginRight": "5px"}),
                html.Span(" to "),
                dcc.Input(id="y-max", type="number", value=default_range[1],
                          style={"width": "80px", "marginLeft": "5px"}),
            ], style={"marginBottom": "10px"}),

            html.Label("Grid Resolution:", style={"fontWeight": "bold"}),
            html.Div([
                dcc.Input(id="sample-number", type="number",
                          value=default_sample_number,
                          style={"width": "100px"}),
            ], style={"marginBottom": "10px"}),

            html.Button(
                "Update Loss Landscape",
                id="update-loss-landscape-button",
                n_clicks=0,
                style={
                    "backgroundColor": "#007bff", "color": "white",
                    "border": "none", "padding": "8px 16px",
                    "borderRadius": "4px", "cursor": "pointer",
                    "fontSize": "14px", "width": "100%",
                },
            ),
        ], style=_card_style()),

        # ── Visibility toggle ───────────────────────────────────────────
        html.Div([
            dcc.Checklist(
                id="show-loss-landscape-toggle",
                options=[{"label": " Show Loss Landscape", "value": LANDSCAPE_SHOW}],
                value=[LANDSCAPE_SHOW],
                labelStyle={"display": "inline-block"},
            ),
        ], style=_card_style()),

        # ── Optimiser settings ──────────────────────────────────────────
        html.Div([
            html.Label("Optimizer:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id="optimizer-name",
                options=[{"label": n, "value": n} for n in optimizers],
                value=first_optimizer_name,
                clearable=False,
                style={"marginBottom": "15px"},
            ),

            html.Label("Learning Rate:", style={"fontWeight": "bold"}),
            dcc.Input(
                id="learning-rate",
                type="number",
                value=first_optimizer.get_default_lr(),
                style={"width": "100px", "marginBottom": "15px"},
            ),

            html.Label("Iterations:", style={"fontWeight": "bold"}),
            dcc.Input(
                id="iterations",
                type="number",
                value=first_optimizer.get_default_iterations(),
                style={"width": "100px", "marginBottom": "15px"},
            ),
        ], style=_card_style()),

        # ── Paths management ────────────────────────────────────────────
        html.Div([
            html.H4("Optimization Paths",
                    style={"marginTop": "10px", "marginBottom": "5px"}),
            html.Div(id="paths-list", children=[]),
            html.Button(
                "Clear All Paths",
                id="clear-paths-button",
                n_clicks=0,
                style={
                    "backgroundColor": "#dc3545", "color": "white",
                    "border": "none", "padding": "4px 8px",
                    "borderRadius": "4px", "cursor": "pointer",
                    "fontSize": "12px", "width": "100%", "marginTop": "10px",
                },
            ),
        ], style=_card_style()),

        # ── Stores ──────────────────────────────────────────────────────
        dcc.Store(id=PATHS_STORE_ID, data=[]),
        dcc.Store(id=LANDSCAPE_VISIBLE_STORE_ID, data=LANDSCAPE_SHOW),
        dcc.Store(id=LOSS_NAME_STORE_ID, data=first_function_name),
        dcc.Store(id="last-click-time", data=0),
        dcc.Store(id="path-counter-store", data=0),  # monotonic counter for path names

    ], style={
        "flex": "0 0 280px",
        "padding": "10px",
        "marginRight": "10px",
        "overflowY": "auto",
    })


def _card_style() -> dict:
    return {
        "backgroundColor": "#f8f9fa",
        "padding": "15px",
        "borderRadius": "8px",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
        "marginBottom": "20px",
    }
