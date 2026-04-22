import torch
from dash import Dash
from python.layout.generate_layout import generate_layout
from python.loss_function import (
    Rosenbrock, Himmelblau, Beale, Booth, Matyas,
    Ackley, Rastrigin, ThreeHumpCamel, Eggholder
)
from python.optimizer import SGD, Adam
from python.callbacks.register_callbacks import register_callbacks

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
    default_sample_number = 100
    app.layout = generate_layout(loss_functions, optimizers, default_sample_number)
    register_callbacks(app, loss_functions, optimizers, default_sample_number)
    app.run(debug=True)