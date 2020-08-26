# Clustering using DBSCAN

## 1.	Summary of algorithm

DBSCAN(Density-Based Spatial Clustering of Applications with Noise) is a data clustering algorithm. It is a density-based clustering algorithm because it finds a number of clusters starting from the estimated density distribution of corresponding nodes.

It starts with an arbitrary starting point that has not been visited.

This points’ epsilon-neighborhood is retrieved, and if it contains sufficiently many points, a cluster is started. Then, a new unvisited point is retrieved and processed, leading to the discovery of a further cluster or noise. DBSCAN requires two parameters: epsilon(eps) and the minimum number of points required to form a cluster(minPts). If a point is found to be part of a cluster, its epsilon-neighborhood is also part of that cluster. 

## 2. Detailed description of codes

### A.	Class Object
i.	Class Object represents data which is known as point in clustering containing index, position(x, y) of the point and whether the point is visited or is already included in cluster, or is classified in noises.

```
class Object:
    def __init__(self, idx, x, y):
        self.idx = int(idx)
        self.x = float(x)
        self.y = float(y)
        self.is_visited = False
        self.in_cluster = False
        self.in_noises = False
```

### B.	Function `density_based_clustering`

This function is a main function in DBSCAN algorithm. It returns clusters in dataset as output by using algorithm with epsilon and min points. 

In for-loop, it finds unvisited point in data set. If the point is found, it becomes visited point. For figuring out whether the point creates a dense part of clusters, the neighborhood surrounding the point within radius is calculated by function `get_neighborhood`. If the number of points in neighborhood is more than threshold, the point becomes a part of new cluster and all points that are found within in neighborhood is used to expand clusters using function `expand_cluster`. If the number of points in neighborhood is less than threshold, the point is regarded as noise. The for-loop is repeated until all points in data set are visited.

```
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
```

### C.	Function `get_neighborhood(point, data_set, radius)`

This function returns neighborhood of point in data set. The neighborhood of point is the list of points which distance between the main point is shorter than radius.

```
def get_neighborhood(point, data_set, radius):
    neighbors = []
    for object in data_set:
        distance = calculate_distance_between_objects(point, object)
        if distance <= radius:
            neighbors.append(object)
    return neighbors
```

### D.	Function `calculate_distance_between_objects(a, b)`

This function is used for calculating distance between two nodes. When detecting whether the distance of two points is further than radius or not in function `get_neighborhood` is required , this function is required.

It simply calculates the distance by Euclidean distance. 

```
def calculate_distance_between_objects(a, b):
    distance = math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2)
    distance = math.sqrt(distance)
    return distance
```

### E.	Function `is_satisfying_threshold(neighbors, threshold)`

This function returns True if the number of points in neighbors is larger than threshold. Or not, it returns False.

```
def is_satisfying_threshold(neighbors, threshold):
    if len(neighbors) >= threshold:
        return True
    else:
        return False
```

### F.	Function `expand_cluster(neighborhood, cluster, data_set, radius, threshold)`

This function is used for expanding cluster which is created before this function is called.

It scans all of unvisited points in neighborhood of the core point to check whether there are more points that can be the parts of same cluster. If one point creates the other part of clusters thanks to satisfying radius and threshold, the neighborhood of that point is joined with neighborhood that we use for scanning unvisited points.

Also, this function makes points not in cluster include in cluster.

```
def expand_cluster(neighborhood, cluster, data_set, radius, threshold):
    for point in neighborhood:
        if point.is_visited is False:
            point.is_visited = True
            point_neighborhood = get_neighborhood(point, data_set, radius)
            if is_satisfying_threshold(point_neighborhood, threshold):
                neighborhood.extend(get_diff_neighbors(neighborhood, point_neighborhood))

        if point.in_cluster is False or point.in_noises is False:
            cluster.append(point)
            point.in_cluster = True
```
