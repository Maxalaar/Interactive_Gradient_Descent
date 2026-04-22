import torch
import numpy as np
from typing import Optional, Tuple

from python.loss_function import LossFunction


def compute_loss_landscape(
    loss_function: LossFunction,
    sample_number: int,
    x_range: Optional[list] = None,
    y_range: Optional[list] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute the loss landscape over a 2-D grid in a single vectorised forward
    pass (no Python-level loop).

    Args:
        loss_function:  LossFunction instance whose ``__call__`` accepts a
                        ``(2, N)`` float32 tensor and returns an ``(N,)`` tensor.
        sample_number:  Number of sample points along each axis.
        x_range:        ``[min, max]`` for parameter 1.  Defaults to
                        ``loss_function.get_parameter_range()``.
        y_range:        ``[min, max]`` for parameter 2.  Defaults to
                        ``loss_function.get_parameter_range()``.

    Returns:
        X, Y, Z:  Three ``(sample_number, sample_number)`` NumPy arrays.
    """
    param_range = loss_function.get_parameter_range()
    if x_range is None:
        x_range = param_range
    if y_range is None:
        y_range = param_range

    x = np.linspace(x_range[0], x_range[1], sample_number)
    y = np.linspace(y_range[0], y_range[1], sample_number)
    X, Y = np.meshgrid(x, y)

    xs = torch.tensor(X.ravel(), dtype=torch.float32)
    ys = torch.tensor(Y.ravel(), dtype=torch.float32)
    params = torch.stack([xs, ys])  # shape (2, sample_number²)

    with torch.no_grad():
        Z_flat = loss_function(params)  # (sample_number²,)

    Z = Z_flat.numpy().reshape(X.shape)
    return X, Y, Z
