
from IPython.display import Javascript, display


# This function generates two new cells at the end of the notebook
# The first cell is a code cell with a call of the pipeline
# The second cell is a code cell generating the widgets to manage states
def generate_widget_cell():
    display(Javascript("const functionCell = Jupyter.notebook.insert_cell_at_bottom('code', 0).set_text('widget_handler.display_function_widgets(dataHandler, pipeline)');"))
    display(Javascript("const widgetCell = Jupyter.notebook.insert_cell_at_bottom('code', 0).set_text('widget_handler.display_data_widgets(dataHandler, pipeline, data)');"))

