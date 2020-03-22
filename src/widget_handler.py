import ipywidgets as widgets
from IPython.core.display import display
import src.cell_generator as cg


# Calling this function generates all widgets for state handling
# It takes a DataHandler object as first param and a Dataframe Object as second param
def display_data_widgets(data_handler, pipeline, data_frame):
    save_intermediate_widget(data_handler, data_frame)
    load_intermediate_widget(data_handler, pipeline)
    export_widget(data_handler, data_frame)
    generate_cell_widget()


def display_function_widgets(data_handler, pipeline):
    create_function_widget(data_handler, pipeline)
    select_function_widget(data_handler, pipeline)


# Calling this function generates the widgets needed for saving data
# It takes a DataHandler object as first param and a Dataframe object as second param
def save_intermediate_widget(data_handler, data_frame):
    # Widgets for qol
    save_button = widgets.Button(description='Save current state',
                                 disabled=False,
                                 button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                 tooltip='Save current data',
                                 icon='save')
    save_input = widgets.Text(placeholder="Enter file name", description="File name:", disabled=False)
    save_box = widgets.HBox([save_input, save_button])

    # save state button
    display(save_box)

    # Helper function that gets called on clicking the button
    # Calls the backend functions for saving
    def on_save_intermediate(b):
        data_handler.save_intermediate(data_frame, save_input.value)
        print("Data saved in: " + save_input.value)

    save_button.on_click(on_save_intermediate)
    return


# Calling this function generates the widgets needed for loading data
# It takes a DataHandler object as param
def load_intermediate_widget(data_handler, pipeline):
    load_button = widgets.Button(description='Load state',
                                 disabled=False,
                                 button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                 tooltip='Load state',
                                 value="",
                                 placeholder="Select file",
                                 icon='arrow-up')
    load_input = widgets.Dropdown(options=data_handler.data_checkpoints, description="File name:", disabled=False)
    load_box = widgets.HBox([load_input, load_button])

    # load button
    display(load_box)

    # Helper function that gets called on clicking the button
    # Calls the backend functions for loading
    def on_load_intermediate(b):
        pipeline.data = data_handler.load_intermediate(load_input.value)
        print("Data loaded from: " + load_input.value)

    load_button.on_click(on_load_intermediate)
    return


# Calling this function generates the widgets needed to export the data as xes
# It takes a DataHandler object as first param and a Dataframe object as second param
def export_widget(data_handler, data_frame):
    export_button = widgets.Button(description='Export as .xes file',
                                   disabled=False,
                                   button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                   tooltip='Export as .xes file',
                                   icon='download')
    export_input = widgets.Text(placeholder="Enter file name", description="File name:", disabled=False)
    export_box = widgets.HBox([export_input, export_button])

    # export button
    display(export_box)

    # Helper function that gets called on clicking the button
    # Calls the backend functions to export as xes
    def on_export(b):
        data_handler.export_to_xes(data_frame, export_input.value)
        print("Data exported to: " + export_input.value)

    export_button.on_click(on_export)
    return


# Calling this function generates the widgets needed to create a function
# It takes a pipeline as argument.
def create_function_widget(data_handler, pipeline):
    create_function_button = widgets.Button(description='Create function',
                                          disabled=False,
                                          button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                          tooltip='Save function')
    function_name_input = widgets.Text(placeholder="Enter function name", description="Command: ", disabled=False)
    function_input = widgets.Textarea(value='# Enter what the function has to execute. Use "self.data" to access to the data\n# self.data.set_index(["concept:instance"], inplace=True)\n'
                                            '# There is no definition needed aswell as no return. Directly start with functionality.',
                                      placeholder='What the function needs to do',
                                      description='Function: ',
                                      disabled=False,
                                      layout= widgets.Layout(width='600px', height='300px'))

    create_box = widgets.VBox([function_name_input, function_input, create_function_button])

    display(create_box)

    # Helper function that gets called on clicking the button
    # Calls the backend functions to export as xes
    def on_create(b):
        pipeline.functions[function_name_input.value] = function_input.value
        data_handler.save_functions(pipeline.functions)
        print("Function saved as " + function_name_input.value)
        print(function_input.value)

    create_function_button.on_click(on_create)
    return


# Calling this function generates the widgets needed to run, show or delete a function
# It takes a pipeline as argument.
def select_function_widget(data_handler, pipeline):
    run_function_button = widgets.Button(description='Run function',
                                            disabled=False,
                                            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                            tooltip='Run function')
    show_function_button = widgets.Button(description='Show function',
                                            disabled=False,
                                            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                            tooltip='Show function')
    delete_function_button = widgets.Button(description='Delete function',
                                          disabled=False,
                                          button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                          tooltip='Delete function')

    function_select = widgets.Dropdown(options=pipeline.functions.keys(), description="Command: ", disabled=False)

    select_box = widgets.HBox([function_select, run_function_button, show_function_button, delete_function_button])

    display(select_box)

    # Helper function that gets called on clicking the button
    #
    def on_run(b):
        pipeline.run(function_select.value)

    # Helper function that gets called on clicking the button
    #
    def on_show(b):
        print("Showing function: " + function_select.value + "\n")
        print(pipeline.functions[function_select.value])

    # Helper function that gets called on clicking the button
    #
    def on_delete(b):
        pipeline.functions.pop(function_select.value, None)
        data_handler.save_functions(pipeline.functions)
        print("Deleted " + function_select.value)

    run_function_button.on_click(on_run)
    show_function_button.on_click(on_show)
    delete_function_button.on_click(on_delete)
    return


# Calling this function generates the widgets needed to generate new cells at the end of the notebook
def generate_cell_widget():
    generate_cell_button = widgets.Button(description='Next step',
                                          disabled=False,
                                          button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
                                          tooltip='Next step')

    display(generate_cell_button)

    # Helper function that gets called on clicking the button
    # Calls the backend functions to generate new cells
    def on_generate(b):
        cg.generate_widget_cell()

    generate_cell_button.on_click(on_generate)
    return
