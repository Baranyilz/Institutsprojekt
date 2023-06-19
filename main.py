import pandapower as pp
import pandapower.topology as top
import pandapower.plotting as plot
import matplotlib.pyplot as plt
from topology_functions import *
networks = []


def import_network():
    try:
        Net_Name = input("Enter the name of the file: ")
        iNet = pp.from_json(Net_Name, convert=True)
        print("Imported network: " + Net_Name + "\n")
        return iNet
    except:
        print("File not found\n")
        return None


def save_network(net, net_name):
    try:
        pp.to_json(net, filename=net_name)
        print("Succesfully exported the network")
    except:
        print("Export failed")


def n_1_contingency_analysis(net):
    # limits
    vmax = 1.05
    vmin = 0.95
    max_ll = 100

    choose_limit = int(input(
        "Which case do you want to check? (1) Default, (2) Feed-in, (3) High-Load "))

    match choose_limit:
        case 1:
            net.sgen.scaling = 1.0
            net.load.scaling = 1.0
        case 2:
            net.sgen.scaling = 0.8
            net.load.scaling = 0.1
        case 3:
            net.sgen.scaling = 0
            net.load.scaling = 0.6
        case _:
            print("Invalid input using default values")
            net.sgen.scaling = 1.0
            net.load.scaling = 1.0

    lines = net.line.index
    critical_lines = list()
    max_voltage = list()
    min_voltage = list()
    line_util = list()

    line_name_input = int(input(
        "Which lines do you want to remove in the analysis: (1) starting_ring_line, (2) ring_line, (3) branch_line, (4) ring_separation_line "))

    line_name = " "

    match line_name_input:
        case 1:
            line_name = "starting_ring_line"
        case 2:
            line_name = "ring_line"
        case 3:
            line_name = "branch_line"
        case 4:
            line_name = "ring_separation_line"
        case _:
            print("Invalid input, removing ring_separation_lines")
            line_name = "ring_separation_line"

    for line in lines:
        # search and remove ring seperation lines iteratively from the network
        if net.line.loc[line, "name"] == line_name:
            net.line.loc[line, "in_service"] = False

        # simulate power flow
        pp.runpp(net, numba=False)

        # check if limits are violated and add line to critical_lines list if so
        if net.res_bus.vm_pu.max() > vmax or net.res_bus.vm_pu.min() < vmin or net.res_line.loading_percent.max() > max_ll:
            critical_lines.append(line)
            max_voltage.append(net.res_bus.vm_pu.max())
            min_voltage.append(net.res_bus.vm_pu.min())
            line_util.append(net.res_line.loading_percent.max())

        # reset the line status
        net.line.loc[line, "in_service"] = True

    for l in critical_lines:
        net.line.loc[l, "parallel"] += 1

    plt.figure()
    plt.scatter(critical_lines, line_util)

    plt.figure()
    plt.scatter(critical_lines, max_voltage)
    plt.scatter(critical_lines, min_voltage)

    plt.show()


def print_networks(list):
    for index, net in enumerate(list):
        print(f"Network at index {index}: {net.name}")


while True:

    print("(1): Import network\n")
    print("(2): Print imported networks\n")
    print("(3): Plot the network\n")
    print("(4): Plot the network (advanced)\n")
    print("(5): N-1 contingency analysis\n")
    print("(6): Save the network\n")
    print("(7): Exit\n")

    User_Input = input("Enter the number of your choice: ")

    match User_Input:
        case "1":
            if len(networks) >= 1:
                import_another_network = input(
                    "Do you want to import another network? (y)es, (n)o ")
                if import_another_network == "y":
                    net = import_network()
                    if net is not None:
                        network_name = input(
                            "Enter the name for the network: ")
                        net.name = network_name
                        networks.append(net)
                elif import_another_network == "n":
                    continue
                else:
                    print("Invalid input")
            else:
                net = import_network()
                if net is not None:
                    network_name = input("Enter the name for the network: ")
                    net.name = network_name
                    networks.append(net)

        case "2":
            print_networks(networks)

        case "3":
            if len(networks) == 1:
                plot.simple_plot(net)
            elif len(networks) > 1:
                print_networks(networks)
                index_network = int(
                    input("Which network do you want to plot? "))
                plot.simple_plot(networks[index_network])
            else:
                print("Please import the network first\n")

        case "4":
            if len(networks) == 1:
                plot.simple_plotly(net)
            elif len(networks) > 1:
                print_networks(networks)
                index_network = int(
                    input("Which network do you want to plot? "))
                plot.simple_plotly(networks[index_network])
            else:
                print("Please import the network first\n")

        case "5":
            if len(networks) == 1:
                n_1_contingency_analysis(net)
            elif len(networks) > 1:
                print_networks(networks)
                index_network = int(
                    input("Which network do you want to analyze? "))
                n_1_contingency_analysis(networks[index_network])
            else:
                print("Please import the network first\n")

        case "6":
            if len(networks) == 1:
                save_network(net, networks[0].name + ".json")
            elif len(networks) > 1:
                print_networks(networks)
                index_network = int(
                    input("Which network do you want to add the line to? "))
                save_network(
                    networks[index_network], networks[index_network].name + ".json")
            else:
                print("Please import the network first\n")

        case "7":
            break

        case _:
            print("Invalid input\n")
