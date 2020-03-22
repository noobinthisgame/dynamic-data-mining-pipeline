

class DynamicPipeline:
    # dictionary of all user-defined functions with "name": "function als plaintext"
    functions = {
        "default_orderbytrace": "self.data.set_index(['concept:instance'], inplace=True)\nself.data.sort_index(inplace=True)",
        "default_orderbytrace_extended": "self.data.set_index(['concept:instance', 'brand', 'channel', 'device', 'sim', 'tariff'], inplace=True)\nself.data.sort_index(inplace=True)"}
    # the referenced main DataFrame
    data = None

    # likely redundant but we're playing it safe
    def __init__(self, data_in):
        self.data = data_in

    # the old "pipeline" function, getting a function object and executing it
    def do(self, function):
        return function(self)

    # default showcase function one: after ungrouped import, group using the trace ID
    def default_orderbytrace(self):
        self.data.set_index(['concept:instance'], inplace=True)
        self.data.sort_index(inplace=True)

    # default showcase function two: after ungrouped import, group using a multiindex
    def default_orderbytrace_extended(self):
        self.data.set_index(['concept:instance', 'brand', 'channel', 'device', 'sim', 'tariff'], inplace=True)
        self.data.sort_index(inplace=True)

    # the new main "pipeline" function, which gets a user-defined function name and executes the appropriate function,
    # which was saved as plain text
    def run(self, name):
        return exec(self.functions[name])
