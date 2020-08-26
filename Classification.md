### Supervised Learning - Classification

- data set of class label is already defined.
- the training data are accompanied by labels indicating classes of observation data.
- new data would be figured out based on training data

### Unsupervised Learning - Clustering

- class label of data is unkown
- given observation, measurements, the aim of processing is estabilishing the existence of classes or clusters in data set

### Data preparation

- data cleaning - 노이즈나 missing value인 애들 제거
- relevance analysis - 관련없거나 중복된 애들 제거함
- data transformation - generalize나 normalize

### Classification Method 측정법

- accuracy
- inpretablity
- scalability : efficiency in disk-resident database
- speed
- robustness

---

## Decision Tree Induction

- 개요
    - greedy algorithm, top down recursive divide-and conquer
    - all attributes should be **categorical  (continuous value should be discritized)**
    - heuristic (gain, gain ratio, gini) / statistical (bayesian)
- 끝나는 순간
    - 모든 attribute가 전부 파티셔닝에 사용되었을 때 → majority voting
    - 더이상 데이터가 없을 때
    - 모든 샘플들이 두 클래스로 잘 나뉘어졌을 때

- 각 method의 한계
    - information gain : multi value를 가진 attribute에 biased
    - gain ratio : tends to split unbalanced partitions that one partition is much smaller than the other.
    - gini index : has difficulty many classes / tends to split partitions that two partitions are equal -sized and purity

- 좋은 점
    - accuracy 못지않게 performance도 중요하지만 decision tree induction의 경우 다른 classification method보다 빠른 learning speed를 보임
    - decision tree induction의 경우 dB에 접근할 때 SQL 쿼리문을 사용할 수 있음
    - 다른 메소드와 비교하면 꽤나 합리적인 accuracy를 보임
    - 그리고 classification rule에 대해서 이해하기 쉽고 simple하게 할 수 있음

---

## Bayesian Classification

- 개요
    - statistical classifier : probabilistic prediction that predicts the membership probability of different classes
    - foundation : bayes' theorem
- 좋은 점
    - 다른 method와 비슷한 performance를 보임
    - incremental : edit data를 처리하기가 쉬움.
    - standard : 다른 method가 주지 못하는 optimal decision의 standard 줄 수 있음
    - computation cost가 적고 구현하기 쉬움
- 안 좋은 점
    - 모든 attribute들이 서로 conditionally independent하다는 가정으로 인해 서로 dependent한 attribute가 있는 실제 상황에서는 사용할 수 없음
    - loss of accuracy

---

## Rule-based Classification

- accuracy 측정법
    - accuracy(R) = N correct / N covers
- conflict resolution
    - size-ordering
    - class-based ordering
    - rule-based ordering(decision list)
- 장점
    - large tree보다 이해하기 쉽다
    - leaf node는 클래스 레이블 말함
    - exclusive , exhaustive

    ---

### Associative Classification

- classification 에 의해서 association rule들이 만들어지거나 분석됨
- 장점
    - deicision tree는 한번에 하나의 attribute에 대해서만 고려하였지만 associative classification을 사용하면 한번에 여러개의 attribute를 고려할 수 있다. →높은 confident association
    - associative classification이 일반 classification보다 더 높은 accuracy

### Eager vs Lazy learning

- instance-based learning
    - k- nearest neighbor approach

---

## Prediction

- regression : predictor, responsive
- linear regression, multilinear regression, nonlinear

### Least Square Method

- w1 =  sum((xi - e(x)) (yi-e(y))) / sum((xi - e(x))^2)
- w0 = e(y) - w1 * e(x)

---

## Accuracy 측정법

### Classification - confusion matrix

- sensitivity : (p-pos) / pos
- specificity : (p-neg) / neg
- precision ; p-pos / (p-pos+p-neg)
- accuracy = sensitivity * pos/(pos+neg) = specificity * neg / (pos+neg)
- accuracy = (t-pos + t-neg) / pos + neg

### Predictor - loss function

- mean absolute error
- mean squared error
- relative absolute error
- relative squared error

### Test set & train set division

- holdout method
- cross validation
- leave-one-out method
- stratified cross-validation
- Boostrap

## Ensemble Method : Increasing the accuracy

- use a combination of models to increase the accuracy

### Bagging

- trainining
    - 각 iteration i마다 Di를 만듦. (replacement를 이용해서 bootstrap)
    - Classifier Mi 는 Di에 의해서 트레이닝 됨
- Classification : majority
- Prediction : average
- accuracy
    - 좋은 결과를 보임
    - outlier에 대하여 robust함

### Boosting
