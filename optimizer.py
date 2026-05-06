from abc import ABC, abstractmethod
from typing import Any, Dict, List

import torch


class Optimizer(ABC):
    """Abstract base class for gradient-based optimisers."""

    def __init__(self) -> None:
        self.default_iterations: int = 1000
        self.name: str = ""

    @abstractmethod
    def create_optimizer(
        self,
        parameters: List[torch.Tensor],
        hyperparams: Dict[str, Any],
    ) -> torch.optim.Optimizer:
        """Instantiate and return the underlying PyTorch optimiser."""
        pass

    def get_default_iterations(self) -> int:
        return self.default_iterations

    def get_hyperparameter_defaults(self) -> Dict[str, Any]:
        """Return a dict of all tunable hyperparameters with default values."""
        return {}


class SGD(Optimizer):
    """Stochastic Gradient Descent with momentum."""

    def __init__(self, momentum: float = 0.9) -> None:
        super().__init__()
        self.name = "SGD"
        self.default_iterations = 1000

    def create_optimizer(
        self,
        parameters: List[torch.Tensor],
        hyperparams: Dict[str, Any],
    ) -> torch.optim.Optimizer:
        lr = hyperparams.get("learning_rate", 0.00001)
        momentum = hyperparams.get("momentum", 0.9)
        return torch.optim.SGD(parameters, lr=lr, momentum=momentum)

    def get_hyperparameter_defaults(self) -> Dict[str, Any]:
        return {"learning_rate": 0.00001, "momentum": 0.9}


class Adam(Optimizer):
    """Adam optimiser."""

    def __init__(self, betas: tuple = (0.9, 0.999)) -> None:
        super().__init__()
        self.name = "Adam"
        self.default_iterations = 1000

    def create_optimizer(
        self,
        parameters: List[torch.Tensor],
        hyperparams: Dict[str, Any],
    ) -> torch.optim.Optimizer:
        lr = hyperparams.get("learning_rate", 0.1)
        beta1 = hyperparams.get("beta1", 0.9)
        beta2 = hyperparams.get("beta2", 0.999)
        return torch.optim.Adam(parameters, lr=lr, betas=(beta1, beta2))

    def get_hyperparameter_defaults(self) -> Dict[str, Any]:
        return {"learning_rate": 0.1, "beta1": 0.9, "beta2": 0.999}