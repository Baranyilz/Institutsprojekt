import pandapower as pp
import pandapower.plotting as plot
import pandas as pd

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
                print("N-1 contingency analysis")
                # TODO
            else:
                print("Please import the network first\n")

        case "5":
            break

        case _:
            print("Invalid input\n")
