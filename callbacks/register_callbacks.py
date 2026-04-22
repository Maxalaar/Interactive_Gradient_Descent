from callbacks.register_on_click import register_on_click
from callbacks.register_sync_loss_function_defaults import register_sync_loss_function_defaults
from callbacks.register_sync_optimizer_defaults import register_sync_optimizer_defaults
from callbacks.register_toggle_loss_landscape_visibility import register_toggle_loss_landscape_visibility
from callbacks.register_update_loss_landscape import register_update_loss_landscape
from callbacks.register_paths_management import register_paths_management
from callbacks.register_cursor_management import register_cursor_management

def register_callbacks(app, loss_functions, optimizers, default_sample_number):
    register_sync_loss_function_defaults(app, loss_functions)
    register_sync_optimizer_defaults(app, optimizers)
    register_on_click(app, loss_functions, optimizers)
    register_update_loss_landscape(app, loss_functions, default_sample_number)
    register_toggle_loss_landscape_visibility(app)
    register_paths_management(app)
    register_cursor_management(app)
