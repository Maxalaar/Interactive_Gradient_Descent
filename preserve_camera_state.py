from typing import Any, Dict, Optional

def preserve_camera_state(figure: Dict[str, Any], relayoutData: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Safely copies the 3D camera state from Plotly's relayoutData
    back into the figure dictionary to prevent unwanted resets.
    """
    # EXACT BLOCK PRESERVED AS REQUESTED
    if relayoutData and "scene.camera" in relayoutData:
        figure["layout"]["scene"]["camera"] = relayoutData["scene.camera"]
    return figure