import csv
import src.csv_processclasses


class FileManager:
    # open all input files and check if opening succeeded
    # should you want to use this notebook for different imports, you need to change this __init__
    def __init__(self):

        self.f0 = open("data/hda_dataset_uniform_random_0.csv", "r")
        if self.f0.mode == 'r':
            print("File 0 opening succeeded")
        else:
            print("File 0 opening failed")

        self.f1 = open("data/hda_dataset_uniform_random_1.csv", "r")
        if self.f1.mode == 'r':
            print("File 1 opening succeeded")
        else:
            print("File 1 opening failed")

        self.f2 = open("data/hda_dataset_uniform_random_2.csv", "r")
        if self.f2.mode == 'r':
            print("File 2 opening succeeded")
        else:
            print("File 2 opening failed")

        self.f3 = open("data/hda_dataset_uniform_random_3.csv", "r")
        if self.f3.mode == 'r':
            print("File 3 opening succeeded")
        else:
            print("File 3 opening failed")

        self.f4 = open("data/hda_dataset_uniform_random_4.csv", "r")
        if self.f4.mode == 'r':
            print("File 4 opening succeeded")
        else:
            print("File 4 opening failed")

        self.f5 = open("data/hda_dataset_uniform_random_5.csv", "r")
        if self.f5.mode == 'r':
            print("File 5 opening succeeded")
        else:
            print("File 5 opening failed")

        self.f6 = open("data/hda_dataset_uniform_random_6.csv", "r")
        if self.f6.mode == 'r':
            print("File 6 opening succeeded")
        else:
            print("File 6 opening failed")

        self.f7 = open("data/hda_dataset_uniform_random_7.csv", "r")
        if self.f7.mode == 'r':
            print("File 7 opening succeeded")
        else:
            print("File 7 opening failed")

        self.fbrands = open("data/brands.csv", "r")
        if self.fbrands.mode == 'r':
            print("File brands opening succeeded")
        else:
            print("File brands opening failed")
        self.fchannels = open("data/channels.csv", "r")
        if self.fchannels.mode == 'r':
            print("File channels opening succeeded")
        else:
            print("File channels opening failed")

        self.fdevices = open("data/devices.csv", "r")
        if self.fdevices.mode == 'r':
            print("File devices opening succeeded")
        else:
            print("File devices opening failed")

        self.fsim = open("data/sim.csv", "r")
        if self.fsim.mode == 'r':
            print("File sim opening succeeded")
        else:
            print("File sim opening failed")

        self.ftariffs = open("data/tariffs.csv", "r")
        if self.ftariffs.mode == 'r':
            print("File tariffs opening succeeded")
        else:
            print("File tariffs opening failed")

    # just close all files. also edit this in case of different import sources!
    def close_all(self):
        self.f0.close()
        self.f1.close()
        self.f2.close()
        self.f3.close()
        self.f4.close()
        self.f5.close()
        self.f6.close()
        self.f7.close()
        self.fbrands.close()
        self.fchannels.close()
        self.fdevices.close()
        self.fsim.close()
        self.ftariffs.close()

    # method to read the aux files using python's csv reader
    @staticmethod
    def read_aux_data(file, dictionary):
        csv_reader = csv.reader(file, delimiter=',')
        first_line = True
        for row in csv_reader:
            if first_line:
                first_line = False
                continue
            dictionary[row[0]] = row[1]

    # method to read the main data, including functionality to detect duplicate traces (but not events!)
    @staticmethod
    def read_data(file, events, existing_case_ids, brands, channels, devices, sims, tariffs):
        csv_reader = csv.reader(file, delimiter=',')
        first_line = True
        c_case_id = -1
        brand_flag = False
        channel_flag = False
        device_flag = False
        sim_flag = False
        tariff_flag = False
        c_brand = str()
        c_channel = str()
        c_device = str()
        c_sim = str()
        c_tariff = str()
        rowcounter = 0
        for row in csv_reader:
            rowcounter += 1
            # skip first line
            if first_line:
                first_line = False
                continue
            # check that it's not a duplicate in the data
            if row[0] in existing_case_ids:
                continue
            # found new case id
            if c_case_id != row[0]:
                # check that we've already done a case
                # if so, reset all used variables
                if c_case_id != -1:
                    existing_case_ids.add(c_case_id)
                    brand_flag = False
                    channel_flag = False
                    device_flag = False
                    sim_flag = False
                    tariff_flag = False

                # get next case ID
                c_case_id = row[0]
                # check for auxiliary data to add since we're enriching every single event with this data
                # this is done to avoid data aggregations at all
                # the auxiliary data is actually pertinent to the trace itself (identified by c_case_id)
                if c_case_id in brands:
                    brand_flag = True
                    c_brand = brands[c_case_id]
                if c_case_id in channels:
                    channel_flag = True
                    c_channel = channels[c_case_id]
                if c_case_id in devices:
                    device_flag = True
                    c_device = devices[c_case_id]
                if c_case_id in sims:
                    sim_flag = True
                    c_sim = sims[c_case_id]
                if c_case_id in tariffs:
                    tariff_flag = True
                    c_tariff = tariffs[c_case_id]

            # always add the event
            c_event = src.csv_processclasses.Event(row[0], row[2], row[1])
            if brand_flag:
                c_event.brand = c_brand
            if channel_flag:
                c_event.channel = c_channel
            if device_flag:
                c_event.device = c_device
            if sim_flag:
                c_event.sim = c_sim
            if tariff_flag:
                c_event.tariff = c_tariff
            events.add(c_event)

        print(rowcounter)
