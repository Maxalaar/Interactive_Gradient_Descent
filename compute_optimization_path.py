import torch
import numpy as np
from typing import List, Dict, Any

from loss_function import LossFunction
from optimizer import Optimizer


def compute_optimization_path(
    loss_function: LossFunction,
    start_parameters: List[float],
    optimizer: Optimizer,
    hyperparams: Dict[str, Any],
    iteration_number: int,
) -> np.ndarray:
    """
    Run gradient-based optimisation from ``start_parameters``.

    Args:
        loss_function:     LossFunction instance.
        start_parameters:  [x0, y0].
        optimizer:         Optimizer instance.
        hyperparams:       Dict of hyperparameters (learning_rate, momentum, etc.)
        iteration_number:  Number of gradient steps.

    Returns:
        Array of shape (iteration_number + 1, 3): [x, y, loss].
    """
    parameters = torch.tensor(start_parameters, dtype=torch.float32, requires_grad=True)
    optimizer_instance = optimizer.create_optimizer([parameters], hyperparams)
    path: List[List[float]] = []

    def record() -> None:
        with torch.no_grad():
            loss = loss_function(parameters)
            path.append([
                parameters[0].item(),
                parameters[1].item(),
                loss.item(),
            ])

    record()

    for _ in range(iteration_number):
        optimizer_instance.zero_grad()
        loss = loss_function(parameters)
        loss.backward()
        optimizer_instance.step()
        record()

    return np.array(path)