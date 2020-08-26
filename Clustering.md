## Clustering이란

### Cluster

- cluster : a collection of data objects
    - similar to one another within the same cluster
    - dissimilar to the objecdts in other clusters
- cluster anaysis :
    - data 에서 찾은 characteristic에따라 data 사이에 similiarity를 찾고, 비슷한 애들끼리 cluster에 그룹핑하는 것

- unsupervised learning

### 사용되는 곳

- standalone-application : spatial data analysis , www, economic science,
- preprocessing step for other algorithms

### 좋은 clustering이란?

- 잘 분류하는 것 : high intra-class similarity & low inter-class similarity → good quality
- hidden pattern을 잘 찾아내는 능력
- 사용하는 메소드에 따라 클러스터링의 결과는 달라짐

### Requirement

- 다양한 attribute를 사용할 수 있는가
- outlier에 robust한가
- scalability한가
- 다이나믹 데이터들을 잘 다룰 수 있는가
- arbitrary shape을 잘 다룰 수 있는가
- input parameter를 굳이 안해도 되는가
- input record 순서에 상관없이 결과가 상관이 없는가
- high dimensionality
- incorporation of user-specified =constraint

---

### Cluster

- a collection of data
- similar to one another within same cluster, but dissmiliar to the objects in other clusters

### Cluster Analysis

- for mining cluster, it finds similarities between data objects according to the characteristic found in the data, and makes groups which has similar data objects

### Major clustering Approaches

- partitioning method
    - construct various partitions and then evalute them by distance based criterion
    - k-mean, k-medoid(PAM, CLARA, CLARANs)
- hierarchical method
    - create a hierarchical decomposition of the set of data using some criterion
    - AGNES, DIANA, BIRCH, ROCK, CHAMELEON
- density-based method
    - bbased on some density functions
    - DBSCAN, OPTICS

### Some properties of clusters

- centroid
    - the middle of center
- radius
    - the root of average of squared distance between the centroid and other objects within same cluster.
- diameter
    - the root of average of squared distance between two of all possible pairs within same cluster.

### cluster 간의 거리를 나타내는 방법들

- single link
    - the minimum distance between an element in cluster and an element in the other.
- complete link
    - the maximum distance between an element in cluster and an element in the other.
- average
    - the average distance between an element in cluster and an element in the other
- centroid
    - the distance between a centroid in cluster and a centroid in the other cluster
- medoid
    - the distance between medoids of two clusters

---

## Partitioning Approach

각 cluster내에서 representative of cluster와 object들의 squared distance 합이 최소가 되도록 n개의 object로 이루어진 데이터 셋에서 k개의 cluster를 partition하는 것이다.

k개의 cluster 개수가 주어지면, 데이터셋을 최적의 cluseter들로 나눌 수 있어야 하는데, global optimal의 경우에는 너무 시간이 많이 걸리기 때문에 heuristic method를 사용해야 한다. k-mean과 k-medoid가 있다.

- 단점 : k라는 cluseter 개수가 정해져있어야 한다.

    ### k-means

    1. 먼저, n개의 object들 중에서 initial cluster center가 될 k개의 seeds를 임의로 정한다. 
    2. 다른 object들과 k개의 seed간의 거리를 구한 후, object들을 더 가깝거나 비슷한 center에 assign 시킨다.(cluster를 만든다.)
    3. 만들어진 cluster의 새로운 centroid를 만든다. 
    4. 2번과 3번을 반복한다 더이상의 변화가 없을 때까지.

    - 장점

        O(n * k * t) 밖에 안 걸린다. k와 t는 n에 비하면 매우 작은 수이기 때문에 linear하게 걸려 efficient하게 처리할 수 있다. (PAM : O(k(n-k)^2) , CLARA : O(ks^2 + (n-k)*k))

    - 약점 : local optimal + outlier + non-convex shapes + no categorical
        - local optimal에 빠질 위험이 있다.
        - mean 의 경우 outlier에 취약하다는 단점이 있다.
        - mean이 define되는 경우만 가능하다. (categorical ? → k-modes)
        - not suitable to discover clusters within non-convex shapes

    ### k-modes

    categorical data object를 다루기 위한 방법이다. mean을 modes로 바꾼다.

    1. 각 attribute마다 가장 자주 발생하는 value값을 측정한다. 이를 Q = <q1, q2, ...qm>에 저장한다.
    2. dist(X, Q) = sum(dist(Xi, Q)) 를 최소화하는 X를 골라 이를 clustering한다. 

    ### k-medoids

    outlier에 취약한 mean 대신에 median으로 representitve of cluster를 정하여 outlier에 좀 더 robust하게 만든다 .

    ### PAM(Partitioning Around Medoids)

    1. k개의 representitve objects를 임의로 고른다. 
    2. seed와 다른 object사이의 거리들을 모두 측정하여 object들이 similar seed에 assign하도록 한다. 
    3. Unselected object h와 selected object i간의 모든 가능한 pair에 대하여 TCih를 계산하여 TCih의 값이 음수일 경우에 i를 h로 바꾼다. 또 다시 seed와 다른 objected와의 거리 측정하여 assign되도록 한다.
    4. 3을 반복한다. 언제까지? 변화가 없을 때까지

    TCih = sum(Cjih) = sum (d(j, h) - d(j, i))

    - 강점 : outlier에 강하다
    - 단점 : 시간복잡도는 O(k(n-k)^2) 이 걸려서 large data set의 경우에는 적합하지 못하다.

    ### CLARA(Clustering Large Applications)

    data set으로부터 multiple sampling을 통해 얻은 sample에 PAM을 적용하여 결과로 가장 좋은 clustering을 준다.

    - 강점 : 큰 data set을 더 잘 다룬다. O(ks^2 + k(n-k))
    - 단점 : sample에 따라 efficiency가 다르다. 만약 샘플에 있어서 좋은 결과를 보이는 클러스터링은 만약 그 샘플이 biased된 것이라면 큰 데이터에 있어서 좋은 결과를 안 보일 수 있다 .

---

## Hierarchical Clustering

- clustering criteria로 distance matrix를 이용함
- clustering 개수 k개가 주어지지 않지만, termination condition을 알아야 함 .

### AGNES(Agglomerative Nesting)

single link를 이용하여 가장 가까운 두 오브젝트끼리 clustering을 bottom-up으로 만드는 방법으로, 모든 object들이 하나의 cluster에 속할 때까지 진행한다. 

- Dendrogram

    data object들을 several levels of nested partitioning으로 decompose한 그림이다. 

    dendrogram을 적절한 desired level로 잘랐을 때 데이터 오브젝트들을 clustering한다. 각 서로 이어져있는 connected object들은 하나의 클러스터에 속한다. 

- n(n-1) / 2
- 시간이 너무 많이 걸리기 때문에 큰 데이터들에 있어서 효율적이지 않다.

### DIANA(Divisive Analysis)

모든 object들을 하나의 클러스터로 만든 후 가장 큰  클러스터를 파티션한다. 이 때 최대한 두 파티션이 같은 크기로 쪼개질 수 있도록 파티션을 하고 모든 클러스터가 하나의 object만을 포함하고 있을 때까지 반복한다. 

- 2^(n-1) -1

complexity를 비교하자면 DIANA가 AGNES보다 초기 단계를 설정할 때 훨씬 더 많은 시간이 걸리므로 heuristic한 방법이 필요하다.

1. 각 오브젝트마다 다른 오브젝트와의 거리를 모두 계산한 후 가장 큰 거리를 가지는 오브젝트 하나를 고른다.(which has the highest dissimilarity within same cluster) 이를 하나의 클러스터로 구분한다.(splinter-group)
2. 해당 오브젝트를 기준으로 splinter group 밖의 모든 object i에 대하여 Di를 계산한다. Di = avg of dist(i, j) ( j 는 Splinter Group에 속해있지 않는 오브젝트들) - avg of dist(i, j) (j는 Splinter Group에 속해있는 오브젝트들)  최대한 Di가 가장 큰 값을 가지는 오브젝트 i가 splinter group에 속하게 된다.
3. DI가 가장 큰 h를 고르는데, 이 h를 splinter group에 포함시킨다. 위의 계산을 반복하는데, Di가 음수가 나올 때까지 반복한다. 
4. 클러스터들 중 가장 diameter가 큰 것을 고른다. diameter는 가장 멀리 떨어져 있는 object들의 거리로 계산된다. 
5. 모든 클러스터들이 하나의 오브젝트만을 가지고 있을때까지 이를 반복한다.

### BIRCH(Balanced Iterative Reducing and Clustering using Hierarchies)

CF Tree를 만드는데, 이는 clustering에 있어서 hierarchical data structure이다.

1. 일단 디비를 한 번 스캔해서, initial in-memory CF tree를 만든다.(각 multi level에 있는 데이터들은 inherent clustering structure of data 를 보존하려고 한다.)
2. 다 만들어진 CF Tree의 leaf node에 있는 클러스터를 clustering analysis를 이용하여 더 큰 클러스터를 만들거나 아니면 micro cluster를 삭제한다. 

- 장점 : 한번의 스캔 만으로도 좋은 clustering을 하고, 몇 번의 스캔을 더 추가하면 더 좋은 클러스터링을 만들 수 있다.
- 단점 : numeric 데이터만 할 수 있다. 데이터 오브젝트의 순서에 민감하다

각 CF Tree의 노드들은 해당 데이터들의 statistical한 정보를 가지고 있다. 

클러스터를 계산하는 데 있어서 정말 좋은 측정방법을 제공하고, 이는 storage를 효율적으로 사용할 수 있다.

CF tree는 hierarchical tree로 height balanced treedl인데, clustering feature를 저장하고 있다. 

### ROCK(Robust Clustering using links)

categorical한 데이터들을 link를 이용하여 클러스터링을 할 수 있음 

jaccard coefficient와 같은 전통적인 방법을 사용하면 정확도에 한계가 있기 때문에 link 정보를 활용한다.

두 오브젝트의 similarity를 비교하기 위해서는 threshold를 만족하는 한 오브젝트의 이웃들과, 다른 오브젝트의 이웃들을 구한 후 각 이웃들이 얼마나 공통되었는지를 측정하는 방법이다. 

### CHAMELEON(Hierarchical Clustering Using Dynamic Modeling)

1. 먼저 오브젝트들을 서로 잇는다. k-nearest-neighbor graph를 형성함. 
    - 오브젝트 기준으로 k개의 가장 가까운 오브젝트들을 해당 오브젝트와 이어 그래프를 형성한다.
2. 형성된 큰 그래프를 파티션 한다.
    - 두개의 sub-cluster로 나누는데, 각 클러스터의 크기가 최대한 동일하게끔 한다. 많은 sub-cluster들을 만든다. (minimize the edge cut(METIS)
3. 파티션된 클러스터들을 이제 합쳐야 한는데, inter connectivity와 closeness를 이용하여 계산한다. internal connectivity와 internal closeness를 비교한다. 

강점 : 임의의 shape 의 cluster를 만드는데 좋은 결과 보임

단점 : high dimensional data에서는 O(N제곱)만큼 걸림, 항상 좋은 결과를 보이는 것은 아님

---

### Density-Based Clustering Method

distance가 아니라 denstiy를 기반으로 하는 클러스터링 방법이다. 

- 강점
    - 임의의 shape를 가진 데이터들을 clustering 가능함
    - 클러스터 개수를 지정할 필요가 없음
    - 한번의 스캔으로 정말 효율적을 돌아감
    - noise를 잘 다룸
- 단점
    - 클러스터의 threshold들이 필요함. density parameter가 필요함
    - density parameter에 따라 생성되는 클러스터가 다름

    ### DBSCAN

    neighborhood의 maximum radius와 neighborhood 내의 최소 object 개수인 Min points 라는 parameter들이 필요하다.

    directly density reachable

    density rechable

    density connected

    density connected한 object들을 최대한 많이 찾는 것이다 

    ### OPTICS(Cluster-Ordering Method)

    density-based clustering structure에 관련하여 디비 내의 object들의 순서들을 생산하는데 파라미터 세팅에 따라 달라지는 클러스터링 스터럭쳐를 보여주는 정보를 제공한다. 

    cluster analysis를 제공하여 유저로 하여금 잘 결정하게끔 하는데, graphically하게 보여진다. 

    core distance와 reachabilitiy distance 

---

## Outlier Analysis

### outlier

outlier란 데이터에 있는 다른 데이터들과 정말 큰 dissimilarity를 보이는 것들. 

statistical outlier analysis는 기존 데이터 분포를 알아야 하고, single attribute에만 해당되기 때문에 density based local outlier detection이 필요하다.
