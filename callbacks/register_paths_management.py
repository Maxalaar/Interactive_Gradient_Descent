import copy
import json
import re

import dash
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from constants import DEFAULT_PATH_COLOR, LANDSCAPE_SHOW, LOSS_LANDSCAPE_TRACE_NAME


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')


def _is_valid_hex(value: str) -> bool:
    return bool(value and _HEX_RE.match(value))


def _path_row(path: dict) -> html.Div:
    """Render one row in the paths list panel."""
    path_id = path["id"]
    color = path.get("color", DEFAULT_PATH_COLOR)

    return html.Div([
        html.Div([
            dcc.Input(
                id={"type": "path-name", "index": path_id},
                type="text",
                value=path["name"],
                style={"width": "110px", "marginRight": "6px"},
            ),
            dcc.Input(
                id={"type": "path-color", "index": path_id},
                type="text",
                value=color,
                placeholder="#rrggbb",
                maxLength=7,
                style={
                    "width": "72px", "marginRight": "4px",
                    "fontFamily": "monospace",
                },
            ),
            html.Div(
                id={"type": "path-color-swatch", "index": path_id},
                style={
                    "width": "20px", "height": "20px",
                    "backgroundColor": color,
                    "border": "1px solid #aaa",
                    "borderRadius": "3px",
                    "display": "inline-block",
                    "verticalAlign": "middle",
                    "marginRight": "6px",
                },
            ),
            dcc.Checklist(
                id={"type": "path-visible", "index": path_id},
                options=[{"label": "visible", "value": "visible"}],
                value=["visible"] if path.get("visible", True) else [],
                labelStyle={"display": "inline-block"},
            ),
            html.Button(
                "✖",
                id={"type": "path-delete", "index": path_id},
                n_clicks=0,
                style={
                    "marginLeft": "6px",
                    "backgroundColor": "#dc3545",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "4px",
                    "cursor": "pointer",
                },
            ),
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"}),
    ], style={"borderBottom": "1px solid #ddd", "marginBottom": "5px"})


def _find_changed_id(ctx) -> dict | None:
    """Return the parsed ``{type, index}`` dict of the triggering component."""
    if not ctx.triggered:
        return None
    raw_id = ctx.triggered[0]["prop_id"].split(".")[0]
    try:
        return json.loads(raw_id)
    except (json.JSONDecodeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Individual callback registrations
# ---------------------------------------------------------------------------

def _register_build_paths_list(app) -> None:
    @app.callback(
        Output("paths-list", "children"),
        Input("paths-store", "data"),
    )
    def build_paths_list(paths):
        if not paths:
            return html.Div(
                "No paths yet. Click on the surface to add one.",
                style={"color": "gray", "fontStyle": "italic"},
            )
        return [_path_row(p) for p in paths]


def _register_update_path_name(app) -> None:
    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-name", "index": dash.dependencies.ALL}, "value"),
        State("paths-store", "data"),
        prevent_initial_call=True,
    )
    def update_path_name(_, current_paths):
        ctx = dash.callback_context
        trigger = _find_changed_id(ctx)
        if trigger is None or trigger.get("type") != "path-name" or not current_paths:
            raise PreventUpdate

        changed_id = trigger["index"]
        new_name = ctx.triggered[0]["value"]

        return [
            {**p, "name": new_name} if p["id"] == changed_id else p
            for p in current_paths
        ]


def _register_update_path_color(app) -> None:
    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-color", "index": dash.dependencies.ALL}, "value"),
        State("paths-store", "data"),
        prevent_initial_call=True,
    )
    def update_path_color(_, current_paths):
        ctx = dash.callback_context
        trigger = _find_changed_id(ctx)
        if trigger is None or trigger.get("type") != "path-color" or not current_paths:
            raise PreventUpdate

        changed_id = trigger["index"]
        new_color = ctx.triggered[0]["value"]

        if not _is_valid_hex(new_color):
            raise PreventUpdate

        return [
            {**p, "color": new_color} if p["id"] == changed_id else p
            for p in current_paths
        ]

    @app.callback(
        Output({"type": "path-color-swatch", "index": dash.dependencies.MATCH}, "style"),
        Input({"type": "path-color", "index": dash.dependencies.MATCH}, "value"),
        State({"type": "path-color-swatch", "index": dash.dependencies.MATCH}, "style"),
        prevent_initial_call=True,
    )
    def update_swatch(new_color, current_style):
        if not _is_valid_hex(new_color):
            raise PreventUpdate
        return {**current_style, "backgroundColor": new_color}


def _register_update_path_visible(app) -> None:
    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-visible", "index": dash.dependencies.ALL}, "value"),
        State("paths-store", "data"),
        prevent_initial_call=True,
    )
    def update_path_visible(_, current_paths):
        ctx = dash.callback_context
        trigger = _find_changed_id(ctx)
        if trigger is None or trigger.get("type") != "path-visible" or not current_paths:
            raise PreventUpdate

        changed_id = trigger["index"]
        new_visible = "visible" in (ctx.triggered[0]["value"] or [])

        return [
            {**p, "visible": new_visible} if p["id"] == changed_id else p
            for p in current_paths
        ]


def _register_delete_path(app) -> None:
    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-delete", "index": dash.dependencies.ALL}, "n_clicks"),
        State("paths-store", "data"),
        prevent_initial_call=True,
    )
    def delete_path(clicks_list, paths):
        if not clicks_list or not paths:
            raise PreventUpdate

        ctx = dash.callback_context
        trigger = _find_changed_id(ctx)
        if trigger is None:
            raise PreventUpdate

        path_id = trigger["index"]
        return [p for p in paths if p["id"] != path_id]


def _register_clear_paths(app) -> None:
    @app.callback(
        Output("surface", "figure", allow_duplicate=True),
        Output("paths-store", "data", allow_duplicate=True),
        Output("path-counter-store", "data", allow_duplicate=True),
        Input("clear-paths-button", "n_clicks"),
        State("surface", "figure"),
        State("surface", "relayoutData"),
        prevent_initial_call=True,
    )
    def clear_all_paths(n_clicks, figure, relayoutData):
        if not n_clicks:
            raise PreventUpdate

        if relayoutData and "scene.camera" in relayoutData:
            figure["layout"]["scene"]["camera"] = relayoutData["scene.camera"]

        return figure, [], 0


def _register_update_figure_from_paths(app) -> None:
    @app.callback(
        Output("surface", "figure", allow_duplicate=True),
        Input("paths-store", "data"),
        Input("landscape-visible-store", "data"),
        State("surface", "figure"),
        State("surface", "relayoutData"),  # <-- added to preserve camera
        prevent_initial_call=True,
    )
    def update_figure_from_paths(paths, landscape_visible, current_figure, relayoutData):
        if current_figure is None:
            raise PreventUpdate

        new_figure = copy.deepcopy(current_figure)

        # Preserve camera position if the user has rotated/zoomed the view
        if relayoutData and "scene.camera" in relayoutData:
            new_figure["layout"]["scene"]["camera"] = relayoutData["scene.camera"]

        # Separate the landscape trace from path traces
        landscape_trace = None
        for trace in new_figure["data"]:
            if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                landscape_trace = trace

        new_data = []
        if landscape_trace is not None:
            landscape_trace["visible"] = (landscape_visible == LANDSCAPE_SHOW)
            new_data.append(landscape_trace)

        new_figure["data"] = new_data

        for path in paths or []:
            if path.get("visible", True):
                path_data = path.get("data")
                if path_data:
                    new_figure["data"].append(
                        go.Scatter3d(
                            x=path_data["x"],
                            y=path_data["y"],
                            z=path_data["z"],
                            mode="markers+lines",
                            marker=dict(size=3, color=path.get("color", DEFAULT_PATH_COLOR)),
                            line=dict(color=path.get("color", DEFAULT_PATH_COLOR), width=2),
                            name=path.get("name", "Path"),
                        ).to_plotly_json()
                    )

        return new_figure


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def register_paths_management(app) -> None:
    _register_build_paths_list(app)
    _register_update_path_name(app)
    _register_update_path_color(app)
    _register_update_path_visible(app)
    _register_delete_path(app)
    _register_clear_paths(app)
    _register_update_figure_from_paths(app)
