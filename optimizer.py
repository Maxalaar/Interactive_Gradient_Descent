from abc import ABC, abstractmethod
from typing import Any, Dict, List

import torch


class Optimizer(ABC):
    """Abstract base class for gradient-based optimisers."""

    def __init__(self) -> None:
        self.default_lr: float = 0.01
        self.default_iterations: int = 100
        self.name: str = ""

    @abstractmethod
    def create_optimizer(
        self,
        parameters: List[torch.Tensor],
        lr: float,
        **kwargs: Any,
    ) -> torch.optim.Optimizer:
        """Instantiate and return the underlying PyTorch optimiser."""
        pass

    def get_default_lr(self) -> float:
        return self.default_lr

    def get_default_iterations(self) -> int:
        return self.default_iterations

    def get_hyperparams(self) -> Dict[str, Any]:
        """
        Return extra hyperparameters that can be surfaced in the UI.

        Each key maps to its current value.  Subclasses should override this
        to expose tunable knobs beyond the learning rate.
        """
        return {}


class SGD(Optimizer):
    """Stochastic Gradient Descent with momentum."""

    def __init__(self, momentum: float = 0.9) -> None:
        super().__init__()
        self.name = "SGD"
        self.default_lr = 0.00001
        self.default_iterations = 100
        self.momentum = momentum

    def create_optimizer(
        self,
        parameters: List[torch.Tensor],
        lr: float,
        **kwargs: Any,
    ) -> torch.optim.Optimizer:
        momentum = kwargs.get("momentum", self.momentum)
        return torch.optim.SGD(parameters, lr=lr, momentum=momentum)

    def get_hyperparams(self) -> Dict[str, Any]:
        return {"momentum": self.momentum}


class Adam(Optimizer):
    """Adam optimiser."""

    def __init__(self, betas: tuple = (0.9, 0.999)) -> None:
        super().__init__()
        self.name = "Adam"
        self.default_lr = 0.1
        self.default_iterations = 100
        self.betas = betas

    def create_optimizer(
        self,
        parameters: List[torch.Tensor],
        lr: float,
        **kwargs: Any,
    ) -> torch.optim.Optimizer:
        betas = kwargs.get("betas", self.betas)
        return torch.optim.Adam(parameters, lr=lr, betas=betas)

    def get_hyperparams(self) -> Dict[str, Any]:
        return {"beta1": self.betas[0], "beta2": self.betas[1]}
