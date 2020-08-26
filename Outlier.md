## Previous Method

### Statistics-based outlier detection

multi-dimensional에 약하고, data distribution을 미리 알고 있어야 함

### Distance-based outlier detection

자기 자신의 object 특성만 고려하고, local density problem을 겪음

global distance threshold를 사용하기 때문에 outlier를 효과적으로 빼낼 수 없음.

### Density-based outlier detection

모든 object들을 특성을 비교하지만, 여전히 micro-cluster를 cluster로 찾는데에 문제가 있음.

## New Method

### Goals

1. outlier를 정확하게 찾아내야 함 - local density, fringe problem, micro-clustering 문제를 해결해야 함
2. user로 하여금 outlier scoreness를 보여서 그들로 하여금 직관적으로 outlier의 수를 결정할 수 있도록 해야 함. 혹은 파라미터 값을 잘 정할 수 있도록 해야 함
3. 어떠한 포맷의 형태의 데이터든 간에 핸들할 수 있어야 함
4. 파라미터 값에 의해서 영향을 받는 것을 최소화해야 함. 갯수를 최소화하던, 아니면 값에 따라서 결과가 크게 바꾸는 일이 없어야 함

### Strategies

1. 데이터셋 내에 있는 모든 오브젝트들의 특성을 고려할 수 있어야 함 
    1. 1번 해결
    2. 파라미터 값에 의해서 영향을 받지 않도록 하는 것이 가능함
2. 주어진 데이터셋을 이용해서 통합한 그래프를 그리고 그래프를 분석하여 outlierness score를 계산할 수 있어야 함
    1. user로 하여금 outlierness score를 보여줄 수 있고
    2. 어떠한 포맷의 혀ㅇ태의 데이터 간에 핸들할 수 있음 

### Procedure

1. k-nn 그래프를 그림
2. center-proximity와 centerality를 계산 해서 outlierness scoree를 계산함 
3. 가장 높은 outlier를 구함 

### Observation

1. cluster center에 가장 가까이 있는 object들은 많은 이웃들을 가지고 있고, 이웃들간의 거리가 가까움
2. outlier는 이와 가까이 있는 오브젝트 수들이 적음

### Scores

### Centrality Score

이는 다른 오브젝트들이 이 오브젝트를 얼마나 센터로 생각하냐는 것을 나타내는 것으로,

- 다른 오브젝트들의 central-proximity가 높을 수록
- 센터로 생각하는 오브젝트 수들이 많을 수록
- 그리고 그 오브젝트들과 거리가 가까울 수록

### Central - proximity Score

해당 오브젝트가 다른 센터들과 얼마나 가까운지를 나타냄 

### Properties

- 서로 mutual reinforcement relationship을 보임
- 가까운 애들일 수록 더 큰 영향력을 보임

### Number of iterations

최대한 converge하게 될때까지 계산을 반복한는 것이 좋다

outlier는 central-proximity를 반대로 해서 구한다

###
