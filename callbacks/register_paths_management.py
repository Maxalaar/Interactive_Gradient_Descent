import copy
import json
import re
from typing import Any, Dict, List, Optional

import dash
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate

from constants import DEFAULT_PATH_COLOR, LANDSCAPE_SHOW, LOSS_LANDSCAPE_TRACE_NAME
from preserve_camera_state import preserve_camera_state

_HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')


def _is_valid_hex(value: str) -> bool:
    return bool(value and _HEX_RE.match(value))


def _get_triggered_id(ctx) -> Optional[Dict[str, Any]]:
    if not ctx.triggered:
        return None
    try:
        return json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    except (json.JSONDecodeError, ValueError):
        return None


def _build_path_row(path: Dict[str, Any]) -> html.Div:
    pid = path["id"]
    color = path.get("color", DEFAULT_PATH_COLOR)
    visible = ["visible"] if path.get("visible", True) else []

    return html.Div([
        dcc.Input(id={"type": "path-name", "index": pid}, value=path["name"],
                  style={"width": "110px", "marginRight": "6px"}),
        dcc.Input(id={"type": "path-color", "index": pid}, value=color, placeholder="#rrggbb",
                  maxLength=7, style={"width": "72px", "marginRight": "4px", "fontFamily": "monospace"}),
        html.Div(id={"type": "path-color-swatch", "index": pid},
                 style={"width": "20px", "height": "20px", "backgroundColor": color,
                        "border": "1px solid #aaa", "borderRadius": "3px",
                        "display": "inline-block", "verticalAlign": "middle", "marginRight": "6px"}),
        dcc.Checklist(id={"type": "path-visible", "index": pid},
                      options=[{"label": "visible", "value": "visible"}],
                      value=visible, labelStyle={"display": "inline-block"}),
        html.Button("✖", id={"type": "path-delete", "index": pid}, n_clicks=0,
                    style={"marginLeft": "6px", "backgroundColor": "#dc3545", "color": "white",
                           "border": "none", "borderRadius": "4px", "cursor": "pointer"}),
    ], style={"display": "flex", "alignItems": "center", "marginBottom": "8px"})


def register_paths_management(app) -> None:
    @app.callback(Output("paths-list", "children"), Input("paths-store", "data"))
    def build_paths_list(paths: List[Dict]):
        return html.Div("No paths yet. Click on the surface to add one.",
                        style={"color": "gray", "fontStyle": "italic"}) if not paths else [_build_path_row(p) for p in
                                                                                           paths]

    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-name", "index": dash.dependencies.ALL}, "value"),
        State("paths-store", "data"), prevent_initial_call=True
    )
    def update_path_name(_, paths):
        ctx = dash.callback_context
        if not ctx.triggered or not paths:
            raise PreventUpdate

        trigger = _get_triggered_id(ctx)
        if not trigger or trigger.get("type") != "path-name":
            raise PreventUpdate

        new_value = ctx.triggered[0].get("value")
        if new_value is None:  # Ignore phantom triggers on component creation
            raise PreventUpdate

        return [{**p, "name": new_value} if p["id"] == trigger["index"] else p for p in paths]

    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-color", "index": dash.dependencies.ALL}, "value"),
        State("paths-store", "data"), prevent_initial_call=True
    )
    def update_path_color(_, paths):
        ctx = dash.callback_context
        if not ctx.triggered or not paths:
            raise PreventUpdate

        trigger = _get_triggered_id(ctx)
        if not trigger or trigger.get("type") != "path-color":
            raise PreventUpdate

        new_value = ctx.triggered[0].get("value")
        if not _is_valid_hex(new_value):
            raise PreventUpdate

        return [{**p, "color": new_value} if p["id"] == trigger["index"] else p for p in paths]

    @app.callback(
        Output({"type": "path-color-swatch", "index": dash.dependencies.MATCH}, "style"),
        Input({"type": "path-color", "index": dash.dependencies.MATCH}, "value"),
        State({"type": "path-color-swatch", "index": dash.dependencies.MATCH}, "style"),
        prevent_initial_call=True
    )
    def update_swatch(new_color: str, current_style: dict):
        if not _is_valid_hex(new_color):
            raise PreventUpdate
        return {**current_style, "backgroundColor": new_color}

    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-visible", "index": dash.dependencies.ALL}, "value"),
        State("paths-store", "data"), prevent_initial_call=True
    )
    def update_path_visible(_, paths):
        ctx = dash.callback_context
        if not ctx.triggered or not paths:
            raise PreventUpdate

        trigger = _get_triggered_id(ctx)
        if not trigger or trigger.get("type") != "path-visible":
            raise PreventUpdate

        new_value = ctx.triggered[0].get("value")
        if new_value is None:  # Guard against initial render
            raise PreventUpdate

        new_visible = "visible" in new_value
        return [{**p, "visible": new_visible} if p["id"] == trigger["index"] else p for p in paths]

    @app.callback(
        Output("paths-store", "data", allow_duplicate=True),
        Input({"type": "path-delete", "index": dash.dependencies.ALL}, "n_clicks"),
        State("paths-store", "data"), prevent_initial_call=True
    )
    def delete_path(clicks_list, paths):
        ctx = dash.callback_context
        if not ctx.triggered or not paths:
            raise PreventUpdate

        # Crucial fix: ignore triggers where n_clicks is 0 (default on component insertion)
        trigger_val = ctx.triggered[0].get("value", 0)
        if trigger_val == 0:
            raise PreventUpdate

        trigger = _get_triggered_id(ctx)
        if trigger and trigger.get("type") == "path-delete":
            return [p for p in paths if p["id"] != trigger["index"]]
        raise PreventUpdate

    @app.callback(
        Output("surface", "figure", allow_duplicate=True),
        Output("paths-store", "data", allow_duplicate=True),
        Output("path-counter-store", "data", allow_duplicate=True),
        Input("clear-paths-button", "n_clicks"),
        State("surface", "figure"), State("surface", "relayoutData"),
        prevent_initial_call=True
    )
    def clear_all_paths(n_clicks, figure, relayoutData):
        if not n_clicks: raise PreventUpdate
        preserve_camera_state(figure, relayoutData)
        return figure, [], 0

    @app.callback(
        Output("surface", "figure", allow_duplicate=True),
        Input("paths-store", "data"),
        Input("landscape-visible-store", "data"),
        State("surface", "figure"),
        State("surface", "relayoutData"),
        prevent_initial_call=True,
        unning=[(Output("cursor-state", "data"), "busy", "idle")],
    )
    def update_figure_from_paths(paths, landscape_visible, current_figure, relayoutData):
        if current_figure is None:
            raise PreventUpdate

        # Update camera in-place (safe, avoids extra dict creation)
        preserve_camera_state(current_figure, relayoutData)

        new_data = []

        # 1️⃣ REUSE the landscape trace object.
        # Plotly.js will skip re-rendering it if the reference/structure is unchanged.
        for trace in current_figure["data"]:
            if trace.get("name") == LOSS_LANDSCAPE_TRACE_NAME:
                trace["visible"] = (landscape_visible == LANDSCAPE_SHOW)
                new_data.append(trace)
                break

        # 2️⃣ Build ONLY the path traces (lightweight dicts)
        for path in (paths or []):
            if path.get("visible", True) and path.get("data"):
                color = path.get("color", DEFAULT_PATH_COLOR)
                new_data.append({
                    "type": "scatter3d",
                    "x": path["data"]["x"],
                    "y": path["data"]["y"],
                    "z": path["data"]["z"],
                    "mode": "markers+lines",
                    "marker": {"size": 3, "color": color},
                    "line": {"color": color, "width": 2},
                    "name": path.get("name", "Path")
                })

        # Return a new figure dict. Reusing current_figure["layout"] avoids
        # serializing layout props and camera state again.
        return {"data": new_data, "layout": current_figure["layout"]}