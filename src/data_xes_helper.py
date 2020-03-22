import pandas as pd
import os
from lxml import etree


# helper function to import a .xes file
def xes_to_dataframe(file_dir, file_name):
    # create xml tree from given file
    xml_tree = etree.parse(file_dir + file_name)
    print("Removing possible prefixes...")
    # since it's possible that tags contain prefixes, we need to remove them for successful importing first
    for element in xml_tree.iter(tag=etree.Element):
        prefix, has_namespace, postfix = element.tag.partition('}')
        if has_namespace:
            element.tag = postfix  # strip all namespaces

    print("Done removing.")
    # do a quick check how many nodes named "trace" exist in the xml structure to verify import integrity
    trace_count = xml_tree.xpath("count(//trace)")
    txt = "Trace count from xpath before actual parsing: {}"
    print(txt.format(trace_count))

    # start the actual parsing at the root
    print("Parsing...")
    xml_root = xml_tree.getroot()

    trace_counter = 0
    columns = []
    rows = []
    rows_index = {}

    # iterate over all nodes with "trace" tag
    for e_trace in xml_root.iter("trace"):
        trace_counter += 1
        event_nodes = []
        event_counter = 0
        # iterate over all nodes of the current trace element
        for event_node in e_trace:
            # check wether the node is the "event" node that needs special investigation.
            # since we want to parse the events last for a nice dataframe structure, temporarily save them
            # in case there are attribute node behind the event node
            if event_node.tag == "event":
                event_counter += 1
                event_nodes.append(event_node)
            # if it isnt an event node, its an attribute with key-value pair
            else:
                key = event_node.get('key')
                value = event_node.get('value')
                if key not in columns:
                    columns.append(key)
                rows_index[key] = value

        # now iterate over the previously saved event nodes
        for event_node in event_nodes:
            event_row = rows_index.copy()
            # every event node has several attribute sub-nodes with key-value pairs.
            # translate empty string to python None
            for e_attribute in event_node:
                key = e_attribute.get('key')
                value = e_attribute.get('value')
                if value == "":
                    value = None
                if key not in columns:
                    columns.append(key)
                event_row[key] = value
            rows.append(event_row)
        txt = "Loaded {} events in trace {}"
        print(txt.format(event_counter, trace_counter))

    print("Done parsing.")

    # actually creating the dataframe is that easy
    pm_dataframe = pd.DataFrame(rows, columns=columns)
    # however, if the trace contained attributes, we can immediately create a multi-indexed dataframe
    # by setting the index to all attributes, to preserve the xes data structure as closely as possible
    if rows_index:
        pm_dataframe.set_index(rows_index.keys(), inplace=True)

    return pm_dataframe


# helper function to extport a dataframe into a .xes file
def dataframe_to_xes(dataframe, file_dir, file_name):
    file_name = file_name + ".xes"
    # quick check so we don't overwrite anything
    if os.path.isfile(file_dir + file_name):
        print("File already exists! Please try again")
        return

    # start the xml structure creation
    print("Creating XML structure...")
    # by defining a root element (tag: log)
    root = etree.Element("log", {"xes.version": "2.0", "xes.features": "",
                                 "xmlns": "http://www.xes-standard.org/"})
    # string "creator" because we're vain
    str_creator = etree.SubElement(root, "string", {"key": "creator", "value": "PSE_HDA_Bohling_Ehlers"})
    print("Converting DataFrame into XML structure - be aware that this may take some time, please be patient")

    # get the dataframe index so we can check for multi-indexing, which means that events are grouped by trace
    df_index = dataframe.index
    if isinstance(df_index, pd.core.index.MultiIndex):
        # assume dataframe is "grouped" by instance (trace), no support for other groupings
        # this requires the label "concept:instance" be present in the dataframe index
        print("Dataframe is multi-indexed, restrictions for export apply. Checking...")
        if 'concept:instance' in df_index.names:
            print("Passed")
            instance_pos = df_index.names.index('concept:instance')
            # so pycharm doesnt cry ("might not be initialized")
            current_instance = -1
            trace = etree.SubElement(root, "trace")
            # iterate over all rows of the dataframe. this is quite time-consuming,
            # since dataframes were not meant for this
            # sadly, dataframes do not inherently support an export to xml (no surprise there)
            for index, row in dataframe.iterrows():
                # check if we reached the next trace
                if index[instance_pos] != current_instance:
                    # so pycharm doesnt cry
                    if current_instance != -1:
                        trace = etree.SubElement(root, "trace")
                    current_instance = index[instance_pos]

                    # if we reached a new trace, we need to put all attributes as nodes into xml first (and only once!)
                    # before we actually add the event nodes
                    i = 0
                    while i < len(index):
                        key = df_index.names[i]
                        value = index[i]
                        i += 1
                        if value is None:
                            value = ""
                        trace_attribute = etree.SubElement(trace, "string", {"key": key, "value": str(value)})

                # regardless of new trace or not, we always add the event with attributes,
                # since a dataframe row is one event
                event = etree.SubElement(trace, "event")
                for key, value in row.iteritems():
                    if value is None:
                        value = ""
                    event_attribute = etree.SubElement(event, "string", {"key": key, "value": value})
        else:
            print("Error: cannot convert multi-indexed dataframe to XES if \'concept:instance\' is not part "
                  + "of the index and \'import_id\' is not at the lowest index level due to XML/XES restrictions."
                  + "\nPlease reformat dataframe for export. Sorry! ")
    # dataframe is nice and easy with no multi index, we simply add every line as an event after a single trace node
    else:
        trace = etree.SubElement(root, "trace")
        for index, row in dataframe.iterrows():
            event = etree.SubElement(trace, "event")
            for key, value in row.iteritems():
                if value is None:
                    value = ""
                attribute = etree.SubElement(event, "string", {"key": key, "value": value})

    # finally, write the structure, using pretty_print
    f = open(file_dir + file_name, "wb")
    print("Writing XML to output file")
    f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
    f.close()

