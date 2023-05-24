import pandapower as pp
import pandapower.plotting as plot
import pandas as pd

import_success = False

while True:

    print("(1): Import network\n")
    print("(2): Plot the network\n")
    print("(3): Plot the network (advanced)\n")
    print("(4): N-1 contingency analysis\n")
    print("(5): Exit\n")

    User_Input = input("Enter the number of your choice: ")

    match User_Input:
        case "1":
            try:
                Net_Name = input("Enter the name of the network: ")
                net = pp.from_json(Net_Name, convert=True)
                print("Network imported successfully\n")
                import_success = True
            except:
                print("File not found\n")

        case "2":
            if import_success:
                plot.simple_plot(net)
            else:
                print("Please import the network first\n")

        case "3":
            if import_success:
                plot.simple_plotly(net)
            else:
                print("Please import the network first\n")

        case "4":
            if import_success:
                print("N-1 contingency analysis")
                # TODO
            else:
                print("Please import the network first\n")

        case "5":
            break
