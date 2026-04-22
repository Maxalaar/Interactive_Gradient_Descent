from dash import html

from create_loss_landscape_figure import create_loss_landscape_figure
from layout.create_graphs_panel import create_graphs_panel
from layout.create_options_panel import create_options_panel

def generate_layout(loss_functions, optimizers, default_sample_number):
    first_function_name = list(loss_functions.keys())[0]
    first_function = loss_functions[first_function_name]
    default_range = first_function.get_parameter_range()

    initial_figure = create_loss_landscape_figure(
        loss_function=first_function,
        x_min=default_range[0],
        x_max=default_range[1],
        y_min=default_range[0],
        y_max=default_range[1],
        sample_number=default_sample_number,
        toggle_value=["show"]
    )

    first_optimizer_name = list(optimizers.keys())[0]
    first_optimizer = optimizers[first_optimizer_name]

    options_panel = create_options_panel(
        loss_functions, optimizers, default_sample_number,
        first_function_name, default_range,
        first_optimizer_name, first_optimizer
    )
    graphs_panel = create_graphs_panel(initial_figure)

    layout = html.Div([
        html.Div(style={
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'right': 0,
            'bottom': 0,
            'margin': 0,
            'padding': 0,
            'height': '100vh',
            'width': '100vw',
            'overflow': 'hidden',
        }, children=[
            html.Div([
                options_panel,
                graphs_panel,
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'nowrap',
                'alignItems': 'stretch',
                'height': '100%',
                'width': '100%',
            })
        ])
    ])

    return layout