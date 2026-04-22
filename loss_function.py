import torch
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Optional


class LossFunction(ABC):
    """Abstract base class for 2-D loss functions."""

    def __init__(self) -> None:
        self.parameter_range: Optional[List[float]] = None
        self.name: Optional[str] = None

    @abstractmethod
    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        """
        Evaluate the loss.

        Supports two calling conventions so the same function works both for
        optimisation (scalar output) and vectorised grid evaluation (batched
        output):

        * **Single point** — ``parameters`` has shape ``(2,)``.
          Returns a scalar tensor.
        * **Batched** — ``parameters`` has shape ``(2, N)``.
          Returns a tensor of shape ``(N,)``.
        """
        pass

    def get_parameter_range(self) -> List[float]:
        """Return the recommended display range ``[min, max]``."""
        return self.parameter_range  # type: ignore[return-value]

    def get_random_initial_point(self, seed: Optional[int] = None) -> List[float]:
        """Return a random starting point within the parameter range."""
        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)

        lo, hi = self.parameter_range  # type: ignore[misc]
        x = np.random.uniform(lo, hi)
        y = np.random.uniform(lo, hi)
        return [x, y]


# ---------------------------------------------------------------------------
# Concrete loss functions
# ---------------------------------------------------------------------------

class Rosenbrock(LossFunction):
    """Global minimum at (1, 1) inside a narrow, curved valley."""

    def __init__(self, a: float = 1, b: float = 100) -> None:
        super().__init__()
        self.a = a
        self.b = b
        self.name = "Rosenbrock Function"
        self.parameter_range = [-2, 3]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        return (self.a - x) ** 2 + self.b * (y - x ** 2) ** 2


class Himmelblau(LossFunction):
    """Four symmetric local minima."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Himmelblau's Function"
        self.parameter_range = [-5, 5]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


class Beale(LossFunction):
    """Deep valley with minimum at (3, 0.5)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Beale Function"
        self.parameter_range = [-4.5, 4.5]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        term1 = (1.5 - x + x * y) ** 2
        term2 = (2.25 - x + x * y ** 2) ** 2
        term3 = (2.625 - x + x * y ** 3) ** 2
        return term1 + term2 + term3


class Booth(LossFunction):
    """Minimum at (1, 3) with gentle slopes."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Booth's Function"
        self.parameter_range = [-10, 10]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


class Matyas(LossFunction):
    """Minimum at (0, 0) with a shallow plateau."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Matyas Function"
        self.parameter_range = [-10, 10]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        return 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y


class Ackley(LossFunction):
    """Global plateau with many local minima."""

    def __init__(self, a: float = 20, b: float = 0.2, c: float = 2 * np.pi) -> None:
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.name = "Ackley Function"
        self.parameter_range = [-5, 5]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        term1 = -self.a * torch.exp(-self.b * torch.sqrt((x ** 2 + y ** 2) / 2))
        term2 = -torch.exp((torch.cos(self.c * x) + torch.cos(self.c * y)) / 2)
        return term1 + term2 + self.a + np.e


class Rastrigin(LossFunction):
    """Highly oscillatory surface with many local minima."""

    def __init__(self, A: float = 10) -> None:
        super().__init__()
        self.A = A
        self.name = "Rastrigin Function"
        self.parameter_range = [-5.12, 5.12]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        return (
            self.A * 2
            + (x ** 2 - self.A * torch.cos(2 * np.pi * x))
            + (y ** 2 - self.A * torch.cos(2 * np.pi * y))
        )


class ThreeHumpCamel(LossFunction):
    """Three humps; global minimum at (0, 0)."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Three-hump Camel Function"
        self.parameter_range = [-5, 5]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        return 2 * x ** 2 - 1.05 * x ** 4 + x ** 6 / 6 + x * y + y ** 2


class Eggholder(LossFunction):
    """Chaotic landscape with many local minima."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Eggholder Function"
        self.parameter_range = [-512, 512]

    def __call__(self, parameters: torch.Tensor) -> torch.Tensor:
        x, y = parameters[0], parameters[1]
        term1 = -(y + 47) * torch.sin(torch.sqrt(torch.abs(y + x / 2 + 47)))
        term2 = -x * torch.sin(torch.sqrt(torch.abs(x - (y + 47))))
        return term1 + term2
