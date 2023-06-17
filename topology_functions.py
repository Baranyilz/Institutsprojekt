import pandapower as pp
import networkx as nx
import pandapower.topology as top
from collections import Counter
import pandapower.networks as pn
import pandapower.plotting as plt
from itertools import islice
import time

net = pp.from_json("example.json")

mg = top.create_nxgraph(net)


def find_branch_buses(net):
    ''' returns the buses which are the first element of a branch with the number of branches as a tuple  
    '''
    bus_list = list()
    lines = net.line.index
    for line in lines:
        if net.line.loc[line, "name"] == "branch_line":
            bus_list.append(net.line.loc[line, "from_bus"])

    return Counter(bus_list)


def lines_connected_with_bus(net, bus):
    ''' returns the index of lines which are connected with the bus in a list  
    '''

    lines = net.line.index
    line_index = list()
    for line in lines:
        if net.line.loc[line, "from_bus"] == bus or net.line.loc[line, "to_bus"] == bus:
            line_index.append(line)

    return line_index


def get_lines_to_bus(net, bus):
    ''' returns the list of the lines which leads to the bus ina list
    '''

    lines = net.line.index
    line_to_bus = list()
    for line in lines:
        if net.line.loc[line, "to_bus"] == bus:
            line_to_bus.append(line)
    return line_to_bus


def get_lines_from_bus(net, bus):
    ''' returns the index of the lines which leads away from the bus in a list
    '''
    lines = net.line.index
    lines_from_bus = list()
    for line in lines:
        if net.line.loc[line, "from_bus"] == bus:
            lines_from_bus.append(line)
    return lines_from_bus


def get_prev_bus(net, bus):
    ''' returns the previous bus of the given bus
    '''

    line_to_bus = get_lines_to_bus(net, bus)
    prev_bus = net.line.loc[line_to_bus[0], "from_bus"]
    return prev_bus


def get_main_bus(net, bus):
    current_bus = bus
    while (net.line.loc[get_lines_to_bus(net, current_bus)[0], "name"] != "starting_ring_line"):
        current_bus = get_prev_bus(net, current_bus)
    return current_bus


def get_prev_bus_nx(mg, bus):
    cc = top.connected_component(mg, bus)
    prev_bus = next(islice(cc, 1, None))
    return int(prev_bus)


def get_main_bus_short(net, bus):
    mg = top.create_nxgraph(net)
    main_buses = list()
    main_bus = None
    lines = net.line.index
    for i in lines:
        if net.line.loc[i, "name"] == "starting_ring_line":
            main_bus = net.line.loc[i, "to_bus"]
            main_buses.append(main_bus)

    min_distance = 500
    for i in main_buses:
        distance = nx.shortest_path_length(mg, i, bus)

        if distance < min_distance:
            min_distance = distance
            nearest_main_bus = i
    return nearest_main_bus

# def get_main_bus_nx(net, mg, bus):
#    '''returns the index of the main bus that is connected to the current bus.
#    net:  pandapower net
#    mg:  networkX map
#    bus: current bus

#    '''
#    current_bus = bus
#    while (net.line.loc[get_line_to_bus(net, current_bus), "name"] != "starting_ring_line"):
#        current_bus = get_prev_bus_nx(mg, current_bus)
#    return current_bus
