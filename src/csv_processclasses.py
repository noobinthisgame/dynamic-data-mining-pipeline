from lxml import etree as lxmletree


class Event:
    # define attributes of an event in our project context
    def __init__(self, caseID, timestamp, description):
        self.caseID = caseID
        self.timestamp = timestamp
        self.description = description
        self.brand = None
        self.channel = None
        self.device = None
        self.sim = None
        self.tariff = None

    # helper function to transform the event into a XES-compliant xml structure
    def xmlify(self, parent):

        # main node
        event = lxmletree.SubElement(parent, "event")

        # xml cannot handle None, it needs an empty string instead
        vbrand = ""
        if self.brand is not None:
            vbrand = self.brand
        vchannel = ""
        if self.channel is not None:
            vchannel = self.channel
        vdevice = ""
        if self.device is not None:
            vdevice = self.device
        vsim = ""
        if self.sim is not None:
            vsim = self.sim
        vtariff = ""
        if self.tariff is not None:
            vtariff = self.tariff

        # create nodes from class attributes
        str_instance = lxmletree.SubElement(event, "string", {"key": "concept:instance", "value": self.caseID})
        str_name = lxmletree.SubElement(event, "string", {"key": "concept:name", "value": self.description})
        str_time = lxmletree.SubElement(event, "date", {"key": "time:timestamp", "value": self.timestamp})
        str_brand = lxmletree.SubElement(event, "string", {"key": "brand", "value": vbrand})
        str_channel = lxmletree.SubElement(event, "string", {"key": "channel", "value": vchannel})
        str_device = lxmletree.SubElement(event, "string", {"key": "device", "value": vdevice})
        str_brand = lxmletree.SubElement(event, "string", {"key": "sim", "value": vsim})
        str_brand = lxmletree.SubElement(event, "string", {"key": "tariff", "value": vtariff})
