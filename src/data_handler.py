import pandas as pd
import os
import pickle
import src.data_xes_helper as data_xes_handler


class DataHandler:

    # init function: default file paths and names
    def __init__(self):
        self.data_checkpoints = []
        self.pickle_dir = "data/pickle/"
        self.pickle_data_unaltered_file_name = "data_unaltered"
        self.xes_dir = "data/xes/"
        self.xes_import_file_name = "events.xes"

    # function to customize the file defaults, called in notebook for easy user access
    def set_variables(self, pickle_dir, pickle_data_unaltered_file_name, xes_dir, xes_import_file_name):
        self.pickle_dir = pickle_dir
        self.pickle_data_unaltered_file_name = pickle_data_unaltered_file_name
        self.xes_dir = xes_dir
        self.xes_import_file_name = xes_import_file_name

    # called once in the first notebook cell to load the original data
    def load_initial_data(self):
        # is there already an unaltered dataframe as pickle at the set default location available?
        # if so, load the default pickled dataframe
        if os.path.isfile(self.pickle_dir + self.pickle_data_unaltered_file_name):
            print(
                "Found preexisting pickle container, delete " + self.pickle_dir
                + self.pickle_data_unaltered_file_name + " to force a reimport from xes")
            self.data_checkpoints.append(self.pickle_data_unaltered_file_name)

            f_data_unaltered = open(self.pickle_dir + self.pickle_data_unaltered_file_name, "rb")
            dataframe = pickle.load(f_data_unaltered)
            f_data_unaltered.close()
        # no pickle found, load from set default .xes file using a helper function containing all xml logic
        else:
            print("Loading data from .xes file: "+ self.xes_dir + self.xes_import_file_name)
            dataframe = data_xes_handler.xes_to_dataframe(self.xes_dir, self.xes_import_file_name)

            f_data_unaltered = open(self.pickle_dir + self.pickle_data_unaltered_file_name, "wb")
            pickle.dump(dataframe, f_data_unaltered, pickle.DEFAULT_PROTOCOL)
            f_data_unaltered.close()

        # also call load_checkpoints to see if there are other pickle files in the specified pickle folder
        self.load_checkpoints()

        return dataframe

    # called by load_initial_data to check for saves pickle checkpoints
    def load_checkpoints(self):
        # check all files in set default pickle directory
        files_in_pickle_dir = [f for f in os.listdir(self.pickle_dir) if os.path.isfile(self.pickle_dir + f)]
        # remove set default original pickle file since that's already loaded
        files_in_pickle_dir.remove(self.pickle_data_unaltered_file_name)
        # ...this one is for us (devs) since we dont add pickle files to git
        files_in_pickle_dir.remove(".gitignore")
        if not files_in_pickle_dir:
            return
        else:
            for f_name in files_in_pickle_dir:
                self.data_checkpoints.append(f_name)
            return

    # this saves the given dataframe as a pickle file in the set default directory
    def save_intermediate(self, dataframe, file_name):
        if not file_name:
            print("Filename cannot be empty")
            return
        # replace any spaces in the filename with underscores (because I like it)
        file_name = file_name.replace(" ", "_")
        f = open(self.pickle_dir + file_name, "wb")
        # automatically add the new checkpoint to list of available checkpoints
        self.data_checkpoints.append(file_name)
        pickle.dump(dataframe, f, pickle.DEFAULT_PROTOCOL)
        f.close()

    # this loads a dataframe from a given pickle file in the default pickle directory
    def load_intermediate(self, file_name):
        f = open(self.pickle_dir + file_name, "rb")
        dataframe = pickle.load(f)
        f.close()
        return dataframe

    # this deletes all pickle files a.k.a. checkpoints which are not the original data within the set default pickle dir
    def clear_all_intermediates(self):
        for file_name in self.data_checkpoints:
            if file_name == self.pickle_data_unaltered_file_name:
                continue
            os.remove(self.pickle_dir + file_name)

        self.data_checkpoints = [self.pickle_data_unaltered_file_name]

    # export current dataframe to .xes file. calls helper function containing all xml logic. beware restrictions
    def export_to_xes(self, dataframe, file_name):
        if not file_name:
            print("Filename cannot be empty")
            return
        file_name = file_name.replace(" ", "_")
        data_xes_handler.dataframe_to_xes(dataframe, self.xes_dir, file_name)
        print("Converted current dataframe to .xes file at " + self.xes_dir + file_name + ".xes")
        print("Please be aware that the created .xes file doesn't include all required meta information "
              + "(global attributes and activity classifiers). Also, all data types are currently set to string."
              + "Neither of these prevents a data reimport, and there should be no loss of data itself."
              + "For further information, please consult the XES Standard Documentation v2.0")
        return

    # save current functions dictionary for persistence, called by editing the functions dictionary in widgets
    def save_functions(self, functions_dict):
        if os.path.isfile("data/functions/functions_save"):
            os.remove("data/functions/functions_save")
        f = open("data/functions/functions_save", "wb")
        pickle.dump(functions_dict, f, pickle.DEFAULT_PROTOCOL)
        f.close()

    # load previously saved functions if they exist
    def load_functions(self, pipeline):
        if os.path.isfile("data/functions/functions_save"):
            f = open("data/functions/functions_save", "rb")
            functions_dict = pickle.load(f)
            f.close()
            if functions_dict:
                pipeline.functions = functions_dict