import torch
import numpy as np
from typing import List

from loss_function import LossFunction
from optimizer import Optimizer


def compute_optimization_path(
    loss_function: LossFunction,
    start_parameters: List[float],
    optimizer: Optimizer,
    learning_rate: float,
    iteration_number: int,
) -> np.ndarray:
    """
    Run gradient-based optimisation from ``start_parameters`` and return the
    full trajectory.

    Args:
        loss_function:     LossFunction instance to minimise.
        start_parameters:  ``[x0, y0]`` starting point.
        optimizer:         Optimizer instance that creates the PyTorch optimiser.
        learning_rate:     Step size passed to the optimiser.
        iteration_number:  Number of gradient steps to take.

    Returns:
        NumPy array of shape ``(iteration_number + 1, 3)`` where each row is
        ``[x, y, loss]``.  Row 0 is the starting point.
    """
    parameters = torch.tensor(start_parameters, dtype=torch.float32, requires_grad=True)
    optimizer_instance = optimizer.create_optimizer([parameters], lr=learning_rate)
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
