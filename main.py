import os
from dash import Dash
from dash.background_callback.managers.diskcache_manager import DiskcacheLongCallbackManager
from diskcache import Cache

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
    # Configuration du gestionnaire pour les callbacks background
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
        debug=not is_production
    )