import sys
import math


class Object:
    def __init__(self, idx, x, y):
        self.idx = int(idx)
        self.x = float(x)
        self.y = float(y)
        self.is_visited = False
        self.in_cluster = False
        self.in_noises = False

    def __str__(self):
        info = "idx : %d (%f, %f %d)" % (self.idx, self.x, self.y, self.is_visited)
        return info


def parse_input_file(input_file):
    objects = []

    f = open(input_file, "r")
    lines = f.readlines()
    for line in lines:
        params = line.split()
        _object = Object(params[0], params[1], params[2])
        objects.append(_object)
    f.close()

    return objects


def calculate_distance_between_objects(a, b):
    distance = math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2)
    distance = math.sqrt(distance)
    return distance


def get_neighborhood(point, data_set, radius):
    neighbors = []
    for object in data_set:
        distance = calculate_distance_between_objects(point, object)
        if distance <= radius:
            neighbors.append(object)
    return neighbors


def is_satisfying_threshold(neighbors, threshold):
    if len(neighbors) >= threshold:
        return True
    else:
        return False


def get_diff_neighbors(main_neighborhood, other_neighborhood):
    set_other = set(other_neighborhood)
    set_main = set(main_neighborhood)

    diff = list(set_other - set_main)
    return diff


def expand_cluster(neighborhood, cluster, data_set, radius, threshold):
    for point in neighborhood:
        if point.is_visited is False:
            point.is_visited = True
            point_neighborhood = get_neighborhood(point, data_set, radius)
            if is_satisfying_threshold(point_neighborhood, threshold):
                neighborhood.extend(get_diff_neighbors(neighborhood, point_neighborhood))

        if point.in_cluster is False and point.in_noises is False:
            cluster.append(point)
            point.in_cluster = True


def density_based_clustering(data_set, num_clusters, radius, threshold):
    clusters = []

    for point in data_set:
        if point.is_visited is False:
            point.is_visited = True
            point_neighborhood = get_neighborhood(point, data_set, radius)

            if is_satisfying_threshold(point_neighborhood, threshold):
                cluster = [point]
                point.in_cluster = True
                expand_cluster(point_neighborhood, cluster, data_set, radius, threshold)

                cluster.sort(key=lambda _o: _o.idx)
                clusters.append(cluster)
            else:
                # point is noise
                point.in_noises = True

    return clusters


def create_output_files(input_file_name, clusters):
    for idx, cluster in enumerate(clusters):
        output_file = input_file_name + "_cluster_" + str(idx) + ".txt"
        f = open(output_file, "w")

        for object in cluster:
            info = str(object.idx) + "\n"
            f.write(info)

        f.close()


def main():
    if len(sys.argv) < 5:
        print("please use command with arguments as below")
        print("input1.txt 8 15 22")
        print("input2.txt 5 2 7")
        print("input3.txt 4 5 5")
        return

    input_file = sys.argv[1]
    n = int(sys.argv[2])
    Eps = float(sys.argv[3])
    MinPts = float(sys.argv[4])

    input_file_name = input_file.split(".")[0]

    data_set = parse_input_file(input_file)

    clusters = density_based_clustering(data_set, n, Eps, MinPts)

    create_output_files(input_file_name, clusters)

    return


if __name__ == "__main__":
    main()
