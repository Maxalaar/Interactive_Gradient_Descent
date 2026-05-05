import os
from dash import Dash
from dash.background_callback.managers.diskcache_manager import DiskcacheLongCallbackManager
from diskcache import Cache

from layout.generate_layout import generate_layout
from loss_function import LossFunction
from optimizer import SGD, Adam
from callbacks.register_callbacks import register_callbacks

# All loss functions as expressions
loss_functions = {
    "Rosenbrock": LossFunction(
        "(1 - x)**2 + 100 * (y - x**2)**2",
        [-2, 3],
        "Rosenbrock Function"
    ),
    "Himmelblau": LossFunction(
        "(x**2 + y - 11)**2 + (x + y**2 - 7)**2",
        [-5, 5],
        "Himmelblau's Function"
    ),
    "Beale": LossFunction(
        "(1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2",
        [-4.5, 4.5],
        "Beale Function"
    ),
    "Booth": LossFunction(
        "(x + 2*y - 7)**2 + (2*x + y - 5)**2",
        [-10, 10],
        "Booth's Function"
    ),
    "Matyas": LossFunction(
        "0.26*(x**2 + y**2) - 0.48*x*y",
        [-10, 10],
        "Matyas Function"
    ),
    "Ackley": LossFunction(
        "-20*exp(-0.2*sqrt((x**2+y**2)/2)) - exp((cos(2*pi*x) + cos(2*pi*y))/2) + 20 + e",
        [-5, 5],
        "Ackley Function"
    ),
    "Rastrigin": LossFunction(
        "10*2 + (x**2 - 10*cos(2*pi*x)) + (y**2 - 10*cos(2*pi*y))",
        [-5.12, 5.12],
        "Rastrigin Function"
    ),
    "Three-hump Camel": LossFunction(
        "2*x**2 - 1.05*x**4 + x**6/6 + x*y + y**2",
        [-5, 5],
        "Three‑hump Camel Function"
    ),
    "Eggholder": LossFunction(
        "-(y+47)*sin(sqrt(abs(y + x/2 + 47))) - x*sin(sqrt(abs(x - (y+47))))",
        [-512, 512],
        "Eggholder Function"
    ),
    "Custom": LossFunction("x**2 + y**2", [-5, 5], "Custom Function"),
}

optimizers = {
    "SGD":  SGD(),
    "Adam": Adam(),
}

if __name__ == "__main__":
    cache = Cache("./.diskcache")
    background_callback_manager = DiskcacheLongCallbackManager(cache)

    app = Dash(__name__, background_callback_manager=background_callback_manager)

    default_sample_number = 100
    app.layout = generate_layout(loss_functions, optimizers, default_sample_number)
    register_callbacks(app, loss_functions, optimizers, default_sample_number)

    is_production = os.environ.get("RENDER") is not None

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=not is_production,
    )