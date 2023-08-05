import math, random
import numpy as np
def get_new_data(x_train, y_train, k_value=5, num_new_data=20) :

    def euclidean_distance(point1, point2):
        sum = 0
        for x in range(len(point1)):
            sum += (point2[x] - point1[x]) ** 2
        sum = math.sqrt(sum)
        return sum

    all_points = {}  # point : label
    for point, label in zip(x_train, y_train):
        all_points[tuple(point)] = label
    # we now need to get the maximum of everycoordinate
    num_dimensions = len(x_train[0])
    maximum_coordinates = []
    for _ in range(num_dimensions):
        maximum_coordinates.append(0)
    minimum_coordinates = []
    for _ in range(num_dimensions)  :
        minimum_coordinates.append(0)
    for point in x_train:
        for cor in range(len(point)):
            if maximum_coordinates[cor] < point[cor]:
                maximum_coordinates[cor] = point[cor]
            if minimum_coordinates[cor] > point[cor] :
                minimum_coordinates[cor] = point[cor]
   # given_desired_new_data_num = 0
    desired_new_data_num = num_new_data
    k_value = 9
    new_points = {}

    for _ in range(desired_new_data_num):
        # the first step is create a new point
        new_point = []
        for x in range(num_dimensions):
            new_point.append(random.uniform(minimum_coordinates[x], maximum_coordinates[x]))

        # print("This is the new_point : ", new_point)

        # the knn_model thing we have to do is go through all the points
        distances_to_points = {}  # distance : point
        for point in all_points:
            distance = euclidean_distance(point, new_point)
            # take this distance and attach it to another dictionary to store it
            distances_to_points[distance] = point

        # right now we need to find the closest points, or the ones with the lowest distances
        sorted_distances_to_points_keys = sorted(distances_to_points)
        sorted_distances_to_points_keys = sorted_distances_to_points_keys[:k_value]
        # now we have the closest distances time to get the closest points
        closest_points = []
        for distance in sorted_distances_to_points_keys:
            closest_points.append(distances_to_points[distance])

        # now that we have the closest points - we need to get their labels from the al_points dict
        closest_points_labels = []
        for point in closest_points:
            closest_points_labels.append(all_points[point])
        new_label = sum(closest_points_labels) / len(closest_points_labels)
        new_points[tuple(new_point)] = new_label

    X, y = [], []
    for given_point, given_label in zip(x_train, y_train):
        X.append(given_point)
        y.append(given_label)

    for point in new_points:
        X.append(list(point))
        y.append(new_points[tuple(point)])

    X, y = np.array(X), np.array(y)
    return X, y
