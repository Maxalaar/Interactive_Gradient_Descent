import os
from dash import Dash
from layout.generate_layout import generate_layout
from loss_function import (
    Rosenbrock, Himmelblau, Beale, Booth, Matyas,
    Ackley, Rastrigin, ThreeHumpCamel, Eggholder
)
from optimizer import SGD, Adam
from callbacks.register_callbacks import register_callbacks

loss_functions = {
    "Rosenbrock": Rosenbrock(),
    "Himmelblau": Himmelblau(),
    "Beale": Beale(),
    "Booth": Booth(),
    "Matyas": Matyas(),
    "Ackley": Ackley(),
    "Rastrigin": Rastrigin(),
    "Three-hump Camel": ThreeHumpCamel(),
    "Eggholder": Eggholder(),
}

optimizers = {
    "SGD": SGD(),
    "Adam": Adam(),
}

if __name__ == "__main__":
    app = Dash(__name__)
    default_sample_number = 10
    app.layout = generate_layout(loss_functions, optimizers, default_sample_number)
    register_callbacks(app, loss_functions, optimizers, default_sample_number)

    is_production = os.environ.get("RENDER") is not None

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050)),
        debug=not is_production
    )