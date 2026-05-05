import torch
import numpy as np
from typing import List, Optional

class LossFunction:
    """
    Loss function defined by a Python expression in 'x' and 'y'.
    Safe evaluation uses a restricted namespace.
    """

    _SAFE_NAMESPACE = {
        "__builtins__": {},
        "abs":   torch.abs,
        "sqrt":  torch.sqrt,
        "exp":   torch.exp,
        "log":   torch.log,
        "sin":   torch.sin,
        "cos":   torch.cos,
        "tan":   torch.tan,
        "sinh":  torch.sinh,
        "cosh":  torch.cosh,
        "tanh":  torch.tanh,
        "pi":    np.pi,
        "e":     np.e,
        "torch": torch,
    }

    def __init__(self, expression: str, parameter_range: List[float], name: str):
        self.expression = expression.strip()
        self.parameter_range = parameter_range
        self.name = name

    def get_expression(self) -> str:
        return self.expression

    def set_expression(self, expression: str) -> None:
        self.expression = expression.strip()

    def get_parameter_range(self) -> List[float]:
        return self.parameter_range

    def validate(self, expression: str) -> Optional[str]:
        """Return an error message if the expression is invalid, else None."""
        try:
            x = torch.tensor(0.5, dtype=torch.float32)
            y = torch.tensor(0.5, dtype=torch.float32)
            ns = {"x": x, "y": y, **self._SAFE_NAMESPACE}
            result = eval(expression, {"__builtins__": {}}, ns)  # noqa: S307
            float(result)
        except Exception as exc:
            return str(exc)
        return None

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        ns = {"x": x, "y": y, **self._SAFE_NAMESPACE}
        return eval(self.expression, {"__builtins__": {}}, ns)  # noqa: S307

    def get_random_initial_point(self, seed: Optional[int] = None) -> List[float]:
        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)
        lo, hi = self.parameter_range
        return [np.random.uniform(lo, hi), np.random.uniform(lo, hi)]