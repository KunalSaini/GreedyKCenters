#! python

import csv
import glob
import random
import math
from functools import reduce
import os
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from os import system, name 


def clear():
    '''
    define console clear function
    '''
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def GetInputDataFile():
    '''
    get user input for which data file to run algo on
    also get number of centroids to compute and whether to
    save scatter plot images or not
    '''
    clear()
    dataFile = None
    k = None
    csvList = glob.glob("data/*.csv")
    print("select a data file to run Lloyd's algorithm")
    for idx, filePath in enumerate(csvList):
        print(f'({idx}) {filePath}')
    dataFileIndex = int(input("select option "))
    if 0 <= dataFileIndex < len(csvList):
        dataFile = csvList[dataFileIndex]
    else:
        GetInputDataFile()

    k = int(input("enter number of clusters to compute "))
    YES_VALUES = {'y', 'yes', 'Y'}
    saveScatterPlots = input("save scatter plot for each iteration ? (y,N) ").lower() in YES_VALUES
    if(saveScatterPlots):
        print('scatter plots will be saved in ./images/ folder')

    print('output csv files will be store in ./output/ folder')
    return (dataFile, k, saveScatterPlots)

def GetDistance(x, y):
    '''
    calculate Euclidean distance between two n dimentional points
    '''
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

def GetDistanceOfAPointFromAllCenters(existingCenters, point):
    closestDistance = math.inf
    for center in existingCenters:
        closestDistance = min(closestDistance, GetDistance(center, point)) 
    return closestDistance

def GetNextCenter(existingCenters, data):
    maxDistance = 0
    nextCenter = None
    for point in data:
        distance = GetDistanceOfAPointFromAllCenters(existingCenters, point)
        if(distance > maxDistance):
            maxDistance = distance
            nextCenter = point
    return (nextCenter, maxDistance)


def ComputeCenters(data, k):
    ## ramdomly select 1 starting point
    centroides = random.sample(data, 1)
    maxDistance = 0
    i = 1
    while i < k :
        nextCenter, maxDistance = GetNextCenter(centroides, data)
        centroides.append(nextCenter)
        i+=1
    return (centroides, maxDistance)

def plotAndSave(plotFileName, centroides, data):
    '''
    create scatter plot
    '''
    #nbrFormat = '{:0>3}'.format(nbr)
    title = 'centers calculated with Greedy K Centers algorithm.'
    fig, ax = plt.subplots(1, figsize=(10, 6))
    ax.set(title=title)
    x = [i[0] for i in data]
    y = [i[1] for i in data]
    ax.scatter(x, y, color='y', s=50)
    for center in centroides:
        ax.scatter(center[0], center[1], color='black', s=50)
    ax.grid(True)
    fig.tight_layout()
    filePath = os.path.join('images', plotFileName)
    plt.savefig(filePath)
    plt.close()

if __name__ == "__main__":
    print("Greedy K Centers")
    dataFile, k, savePlot = GetInputDataFile()
    
    print(f"reading file from {dataFile}")
    data = []
    with open(dataFile, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            dataRow = [float(row[0]),float(row[1])]
            data.append(dataRow)
    
    centroides, objFunctionValue = ComputeCenters(data, k)
    print('centroides', centroides)
    print('objective function value', objFunctionValue)
    if savePlot:
        _, tail = os.path.split(dataFile)
        plotFileName = tail + '.scatterplot.png'
        plotAndSave(plotFileName, centroides, data)