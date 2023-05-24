import pandapower as pp
import pandapower.plotting as plot
import pandas as pd
import matplotlib.pyplot as plt

import_successful = False


def import_network():
    try:
        Net_Name = input("Enter the name of the network: ")
        iNet = pp.from_json(Net_Name, convert=True)
        print("Imported network: " + Net_Name + "\n")
        return iNet
    except:
        print("File not found\n")
        return None


def n_1_contingency_analysis(net):
    # limits
    vmax = 1.05
    vmin = 0.95
    max_ll = 100

    lines = net.line.index
    critical_lines = list()

    for line in lines:
        # search and remove ring seperation lines iteratively from the network
        if net.line.loc[line, "name"] == "ring_seperation_lines":
            net.line.loc[line, "in_service"] = False

        # simulate power flow
        pp.runpp(net, numba=False)

        # check if limits are violated and add line to critical_lines list if so
        if net.res_bus.vm_pu.max() > vmax or net.res_bus.vm_pu.min() < vmin or net.res_line.loading_percent.max() > max_ll:
            critical_lines.append(line)

        # reset the line status
        net.line.loc[line, "in_service"] = True

    # print the critical_lines lines
    print(critical_lines)

    line_util = []
    max_voltage = []
    min_voltage = []

    for i in critical_lines:
        line_util.append(net.res_line.loc[i, "loading_percent"])
        net.line.loc[i, "in_service"] = False

        pp.runpp(net, numba=False)

        max_voltage_bus = net.res_bus.vm_pu.max()
        min_voltage_bus = net.res_bus.vm_pu.min()
        max_voltage.append(max_voltage_bus)
        min_voltage.append(min_voltage_bus)

        net.line.loc[i, "in_service"] = True

    plt.figure()
    plt.scatter(critical_lines, line_util)
    plt.xlabel("Out of Service Line Index")
    plt.ylabel("Line Utilization (%)")
    plt.title("Line Utilization for Critical Lines")

    plt.figure()
    plt.scatter(critical_lines, max_voltage)
    plt.xlabel("Out of Service Line Index")
    plt.ylabel("Voltage (pu)")
    plt.title("Max Voltage in the Network for N-1 Cases")

    plt.scatter(critical_lines, min_voltage)
    plt.xlabel("Out of Service Line Index")
    plt.ylabel("Voltage (pu)")
    plt.title("Min/Max Voltage in the Network for N-1 Cases")

    plt.show()


while True:

    print("(1): Import network\n")
    print("(2): Plot the network\n")
    print("(3): Plot the network (advanced)\n")
    print("(4): N-1 contingency analysis\n")
    print("(5): Exit\n")

    User_Input = input("Enter the number of your choice: ")

    match User_Input:
        case "1":
            if import_successful:
                override = input(
                    "A network is already imported. Do you want to override it? (y/n): ")
                if override == "y":
                    net = import_network()
                    if net is not None:
                        import_successful = True
                else:
                    print("Network import cancelled\n")
            else:
                net = import_network()
                if net is not None:
                    import_successful = True
        case "2":
            if import_successful:
                plot.simple_plot(net)
            else:
                print("Please import the network first\n")

        case "3":
            if import_successful:
                plot.simple_plotly(net)
            else:
                print("Please import the network first\n")

        case "4":
            if import_successful:
                n_1_contingency_analysis(net)
            else:
                print("Please import the network first\n")

        case "5":
            break

        case _:
            print("Invalid input\n")
