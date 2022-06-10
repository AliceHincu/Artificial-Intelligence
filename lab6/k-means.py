import csv
import math
import random
import numpy as np
import matplotlib.pyplot as plt

numberOfClusters = 4


def readCSV(fileName):
    result = {}
    points = []
    with open(fileName) as csv_file:
        spam_reader = csv.reader(csv_file)
        for row in spam_reader:
            if row[0] == 'label':
                continue
            points.append((float(row[1]), float(row[2])))
            result[(float(row[1]), float(row[2]))] = row[0]
    return result, points


def selectInitialCentroids(elements, k=numberOfClusters):
    """
    Select k random "coordinates" from dataset.csv to be the initial centroids
    :param elements: the points
    :param k: nr of clusters
    :return: list with 4 centroisd
    """
    result = []
    for i in range(k):
        result.append(random.choice(elements))
    return result


def euclideanDistance(pointA, pointB):
    """ The length of a line segment between the two points.
    It can be calculated from the Cartesian coordinates of the points using the Pythagorean theorem,
    """
    return np.linalg.norm(np.array(pointA) - np.array(pointB))


def assignPointsToCentroid(points, centroids):
    """
    Calculate the euclidean distance from a point to every centroid...if the current centroid is closer than the
    last one, update de minimum distance and add the point to this centroid too.
    """
    assignedLabel = {}
    for centroid in centroids:
        assignedLabel[centroid] = []

    for point in points:
        minDistance = np.inf
        for centroid in centroids:
            if euclideanDistance(point, centroid) < minDistance:
                assignedLabel[centroid].append(point)
                minDistance = euclideanDistance(point, centroid)
    return assignedLabel


def computeMeanX(points):
    """Average X coordinate"""
    return np.mean([point[0] for point in points])


def computeMeanY(points):
    """Average y coordinate"""
    return np.mean([point[1] for point in points])


def recomputeCentroid(clusters, centroids):
    """
    Here we have 4 clusters from the old centroids. By computing the means, we can find new centroids.
    """
    newCentroids = []

    for centroid in clusters.keys():
        currentCluster = clusters[centroid]
        newCentroid = (computeMeanX(currentCluster), computeMeanY(currentCluster))
        newCentroids.append(newCentroid)

    return newCentroids


def conditionToStopKMean(centroids, newCentroids):
    """
    Stop when the centroids will not update anymore.
    """
    if centroids == newCentroids:
        return True
    return False


def solve():
    # read the data
    data, points = readCSV("dataset.csv")

    finalLabels = {}

    # The Dunn Index (DI) is one of the clustering algorithms evaluation measures. It is most commonly used to
    # evaluate the goodness of split by a K-Means clustering algorithm for a given number of clusters.
    # The Dunn index is calculated as a ratio of the smallest inter-cluster distance to the largest intra-cluster
    # distance.
    finalDunnIndex = -np.inf
    for i in range(10):
        random.seed(i * 25 + 956 / (i + 1))
        # select 4 random centroids, assign the points to those 4 centroids, then recompute the new centroids based on
        # the mean coordinates.
        centroids = selectInitialCentroids(points)
        assignedLabel = assignPointsToCentroid(points, centroids)
        newCentroids = recomputeCentroid(assignedLabel, centroids)
        while not conditionToStopKMean(centroids, newCentroids):
            # repeat until the old centroids are the same as the new centroids.
            centroids = newCentroids
            assignedLabel = assignPointsToCentroid(points, centroids)
            newCentroids = recomputeCentroid(assignedLabel, centroids)

        # We need the minimum distance between two clusters
        interClusterDistance = min(
            [euclideanDistance(centroids[a], centroids[b]) for a in range(len(centroids)) for b in
             range(a + 1, len(centroids))])

        # the distance among members of a cluster -> This metric gives a sense of how well the distance measure
        # was able to bring the items together. Intra-cluster distance is a measure of how close the points lie to each
        # other. We need the maximum distance between two points in the same cluster
        intraClusterDistance = max([euclideanDistance(point, centroid) for centroid in assignedLabel.keys() for point in
                                    assignedLabel[centroid]])


        currentDunnIndex = interClusterDistance / intraClusterDistance
        print("The dunn index for iteration ", i, " is", currentDunnIndex)

        # A high DI means better clustering since observations in each cluster are closer together, while clusters
        # themselves are further away from each other.
        if finalDunnIndex < currentDunnIndex:
            finalDunnIndex = currentDunnIndex
            finalLabels = assignedLabel
        finalPlot(assignedLabel)

    finalPlot(finalLabels)
    statistics(finalLabels, data, giveValueToEachCentroid(finalLabels))


def giveValueToEachCentroid(assignedLabels):
    centroids = list(assignedLabels.keys())
    centroidA = min(centroids, key=lambda x: x[0])
    centroids.remove(centroidA)

    centroidC = max(centroids, key=lambda x: x[0])
    centroids.remove(centroidC)

    centroidD = min(centroids, key=lambda x: x[1])
    centroids.remove(centroidD)

    return {centroidA: 'A', centroids[0]: 'B', centroidC: 'C', centroidD: 'D'}


def finalPlot(assignedLabels):
    """
    Plot the 4 clusters
    :param assignedLabels:
    :return:
    """
    colours = ['red', 'green', 'blue', 'purple']
    index = 0
    for key in assignedLabels:
        plt.scatter(
            [point[0] for point in assignedLabels[key]],
            [point[1] for point in assignedLabels[key]],
            c=colours[index]
        )
        index += 1

    plt.scatter([centroid[0] for centroid in assignedLabels], [centroid[1] for centroid in assignedLabels], c='black')
    plt.show()


def statistics(assignedLabels, initialData, mappedCentroids):
    correctlyComputed = 0
    correctForLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    totalForLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    totalInitialLabel = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

    # if the label of the initial data is the same as the final data => final data for that point is correct
    for key, value in assignedLabels.items():
        for val in value:
            if initialData[val] == mappedCentroids[key]:
                correctlyComputed += 1
                correctForLabel[initialData[val]] += 1
            totalForLabel[mappedCentroids[key]] += 1
            totalInitialLabel[initialData[val]] += 1

    accuracyIndex = correctlyComputed / len(initialData)
    print("Accuracy index:", accuracyIndex)

    precision = {}
    rappel = {}
    score = {}
    for key in ['A', 'B', 'C', 'D']:
        precision[key] = correctForLabel[key] / totalForLabel[key]
        rappel[key] = correctForLabel[key] / totalInitialLabel[key]
        score[key] = 2 * precision[key] * rappel[key] / (precision[key] + rappel[key] + 1)

    print("Precision:", precision)
    print("Rappel:", rappel)
    print("Score:", score)

solve()