import pandapower as pp
import networkx as nx
import pandapower.topology as top
from collections import Counter

net = pp.from_json("example.json")


def find_branch_buses(net):
    bus_list = list()
    lines = net.line.index
    for line in lines:
        if net.line.loc[line, "name"] == "branch_line":
            bus_list.append(net.line.loc[line, "from_bus"])

    return Counter(bus_list)


def lines_connected_with_bus(net, bus):
    lines = net.line.index
    line_index = list()
    for line in lines:
        if net.line.loc[line, "from_bus"] == bus or net.line.loc[line, "to_bus"] == bus:
            line_index.append(line)

    print(line_index)


mg = top.create_nxgraph(net)
print(nx.shortest_path(mg, 1, 2))

# cc = top.connected_component(mg, 188)

# for item in cc:
#    print(item)
lines_connected_with_bus(net, 1)
lines_connected_with_bus(net, 414)
lines_connected_with_bus(net, 413)
lines_connected_with_bus(net, 415)
