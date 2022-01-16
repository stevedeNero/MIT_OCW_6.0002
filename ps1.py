###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
from collections import OrderedDict
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    #Initialize the returned list-of-lists 
    result = []

# =============================================================================
# #the following lambda function provides a more graceful solution to ordering the lists. 
# # It was suggested in the comments section of the discussion to PSET1
# #    cow_dict = OrderedDict(sorted(cows.items(), key=lambda item: item[1], reverse = True))
# =============================================================================
    
    
    #Begin First Successful Attempt 

    # First, we create a copy of the Cow Dictionary - AND -
    # A new dictionary to keep track of which cows have been taken away.
    cowsTransported = []
    copyCows = cows.copy()
    
    cowNames = []
    
    #Create list of sorted values (weights). Largest First --> Smallest Last
    cowWeights = sorted(cows.values(),reverse=True) 
    #Create copy of cow dictionatry sorted by values descending 
    for weight in cowWeights: 
        for key, value in cows.items(): 
            if value == weight and key not in cowNames: 
                cowNames = cowNames + [key]
    #Now, the cowNames and cowWeights are in the same order of descending weight
    
    print('List of Weights')
    print(cowWeights)
    print('List of Names')
    print(cowNames)
    print()
    
    #while loop to make sure you get all your cows that can fit on a ship
    while (len(cowsTransported) < len(cows)) and (limit >= min(copyCows.values())):
        print('Begin New While Loop')
        #Initialize how much weight this trip has taken so far
        totalCost = 0
        cowsThisTrip = []
        for i, weight in enumerate(cowWeights):
            print('Weight',weight,'i',i,'Considering ',cowNames[i])
            if cowNames[i] not in cowsTransported:
                if (totalCost + weight) <= limit:
                    cowsThisTrip = cowsThisTrip + [cowNames[i]]
                    cowsTransported = cowsTransported + [cowNames[i]]
                    totalCost += weight
                    del(copyCows[cowNames[i]])
        result.append(cowsThisTrip)

    #End First Successful Attempt. 
    
    return result


# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    copyCows = cows.copy()
    minTrips = 30000
    result = []
    # validTransport = []
    
    for branch in (get_partitions(copyCows.keys())):
        validBranchVals = 0
        for transport in branch:
            totalWeight = 0
            for i in range(len(transport)):
                totalWeight += copyCows[transport[i]]
            if totalWeight <= limit:
                #validTransport.append(transport)  #Memoization. Add this check in earlier if you want.
                validBranchVals += 1
        if validBranchVals == len(branch):
            if len(branch) < minTrips:
                print()
                print('Successful Branch:',len(branch),'trips:  ',branch)
                result = branch
                minTrips = len(branch)
    
    return result

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    startGreedy = time.time()
    print(greedy_cow_transport(cows, 10))
    endGreedy = time.time()
    
    startBrute = time.time()
    print(brute_force_cow_transport(cows, 10))
    endBrute = time.time()
    
    print('Greedy Time Required:',endGreedy - startGreedy)
    print('Brute Force Time Required:',endBrute - startBrute)

"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
# print(cows)
# print(greedy_cow_transport(cows, limit))
# print(brute_force_cow_transport(cows, limit))
compare_cow_transport_algorithms()

