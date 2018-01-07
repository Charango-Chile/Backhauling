# Import PuLP modeler functions
from pulp import *
import pandas as pd
import numpy as np


def main_run(distancias, trucks):

# def main_run():
#     distancias = pd.read_csv('C:/Users/chara/OneDrive/Desktop/Thailand_Backhauling_Docos/Distances.csv', header=None)
#     trucks = pd.read_csv('C:/Users/chara/OneDrive/Desktop/Thailand_Backhauling_Docos/TruckList.csv', header = None)

    file = open('C:/Users/chara/Backhauling/OptDemoNov/static/data/results_opt.txt', 'w')

    # TODO: Incorporate types of Truck and Types of Products - This require changes in the modal form!
    # For the purposes of the demo this will not be considered

    # TODO: Change fixed cost later on - remember that needs to be read from a database and is particular to each truck
    Transport_Cost = 3.0 # Baht per Kilometer, default at this point of the demo
    Transport_Price = 2.0 # Baht per Kilogram per Kilometer, default at this point of the demo
    Loading_time = 15 # TODO: Use this later
    Unloading_time = 8 # TODO: Use this later

    trucks.columns =  ["Latitude", "Longitude", "Type", "Index", "Capacity", "GlobalIndex"]

    free_zone_index = trucks['GlobalIndex'].idxmax()

    ProblemTrucks = trucks[trucks.Type == "Truck"] # Dataframe with Trucks, GlobalIndex gives their position for the distance matrix
    ProblemParcels = trucks[trucks.Type == "Parcel"] # Dataframe with Parcels, GlobalIndex gives their position for the distance matrix
    ProblemTrucks.is_copy = False
    ProblemParcels.is_copy = False

    ProblemTrucks['CapAdjusted'] = np.where(ProblemTrucks['Capacity'] == 0, '10', ProblemTrucks['Capacity'])
    ProblemParcels['CapAdjusted'] = np.where(ProblemParcels['Capacity'] == 0, '2', ProblemParcels['Capacity'])

    truckCapacities = []

    ProblemTrucksIndexes = ProblemTrucks['GlobalIndex'].values.tolist()
    ProblemParcelsIndexes = ProblemParcels['GlobalIndex'].values.tolist()

    ProblemNodes = trucks["GlobalIndex"].tolist()
    ProblemTrucksCapacities = ProblemTrucks["Capacity"].tolist()
    ProblemParcelsCapacities = ProblemParcels["Capacity"].tolist()
    ProblemCapacities = trucks["Capacity"].tolist()
    ProblemDistances = distancias.values.tolist()

    Indexes = list(itertools.product(ProblemParcelsIndexes, ProblemNodes, ProblemTrucksIndexes))
    # Create the 'prob' variable to contain the problem data, the objective is to maximize!
    prob = LpProblem("The Backhauling Problem", LpMaximize)

    # A dictionary called 'Routing_vars' is created to contain the referenced Variables
    Routing_vars = LpVariable.dicts("X", ((i, j, k) for i, j, k in Indexes), cat='Binary')

    # The objective function is added to 'prob' first
    prob += lpSum([(Transport_Price*ProblemCapacities[j]*ProblemDistances[i][j] - Transport_Cost*ProblemDistances[i][j])*Routing_vars[i, j, k] - Transport_Cost*ProblemDistances[k][free_zone_index]*Routing_vars[i,free_zone_index,k] for i, j, k in Indexes]), "Total Travel Profit"\

    # The constraints are added to 'prob'
    for k in ProblemTrucksIndexes:
        prob += lpSum([Routing_vars[free_zone_index, j, k] for j in ProblemNodes]) == 1, "Trucks Free Zone Go Somewhere " + str(k)

    for k in ProblemTrucksIndexes:
        for i in ProblemParcelsIndexes:
            prob += lpSum([Routing_vars[i, j, k] for j in ProblemNodes]) <= 1, "Things can be Put in One Truck at Most (" + str(k) +", " + str(i) + ")"

    for j in ProblemNodes:
        prob += lpSum([Routing_vars[i, j, k] for i, k in list(itertools.product(ProblemParcelsIndexes, ProblemTrucksIndexes))]) == 1, "From Parcel Location Going Somewhere " + str(j)

    # for i in ProblemParcelsIndexes:
    #     prob += lpSum([Routing_vars[i, j, k] for j, k in list(itertools.product(ProblemNodes, ProblemTrucksIndexes))]) <= 1, "Coming from Somewhere " + str(i)

    for k in ProblemTrucksIndexes:
        prob += lpSum([Routing_vars[i, k, k] for i in ProblemParcelsIndexes]) == 1, "Truck " + str(k) + "Every Truck Finishes Route on Depot"

    # for k in ProblemTrucksIndexes:
    #     prob += lpSum([Routing_vars[i, j, k]*ProblemCapacities[j] for i, j in list(itertools.product(ProblemNodes, ProblemNodes))]) <= ProblemCapacities[k], "Capacity Constraint for all Trucks " + str(k)

    # The problem data is written to an .lp file
    prob.writeLP("BackhaulingModel.lp")

    # print(prob)

    # The problem is solved using PuLP's choice of Solver
    prob.solve(pulp.GLPK())


    # The status of the solution is printed to the screen
    #file.write("Status:" + str(LpStatus[prob.status]) + "\n")

    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        if v.varValue > 0:
            file.write(str(v.name)+  "=" +  str(v.varValue) + ", ")

    file.write('\n')
    file.write('\n')
    file.write('\n')


    # The optimised objective function value is printed to the screen
    file.write("Total Value of Obj. Function = "+ str(value(prob.objective))+ "\n")

    file.close()



if __name__ == '__main__':
    main_run()