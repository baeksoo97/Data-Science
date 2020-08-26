## Frequent Pattern

1. frequent pattern 정의, 중요한 이유
2. association rule 과 support, confidence
3. close, max pattern 정의, 등장 이유
    - 너무 많은 frequent pattern을 쉽게 표현하기 위해서
    - close pattern = lossless compression of frequent patterns for reducing the number of frequent patterns and rules
4. Frequent Pattern 속성
    - frequent pattern들의 subset들은 반드시 frequent하다
5. Frequent Pattern Mining Tool
    - Apriori

## Frequet Pattern Mining 1 - Apriori

1. candidate를 generate하고 support를 만족하는지 테스트하여 접근하는 알고리즘
2. 속성 : infrequent한 pattern들의 superset 또한 infrequent함.
3. **Apriori pruning principle** : infrequent한 pattern들에 대한 superset들을 절대로 generate하거나 테스트하지 않음.
4. 원리 : a candidate-generation and test approach
    - DB를 스캔해서 frequent-1-itemset을 만듦
    - frequent-k-itemset으로부터 candidate-k+1-itemset들을 생성함(join&prune)
    - candidate-k+1-itemset DB scan 통해 min_support를 만족하는지 테스트하여 frequent-k+1만듦
    - candidate, frequent 없을 때까지 반복
5. 코드

    ```python
    L1 = {frequent itemset}
    for (k = 1; Lk != NULL; k++):
    	Ck+1 = generate_candidates_from_L(Lk) 
    	// L로부터 join & prune 작업을 함 
    	// join : 서로 합쳐 일단 후보를 만듬
    	// prune : 너무 많은 후보를 subset을 조사하여 삭제
    	
    	for transaction t in DB:
    		increment the count of all candidates in Ck+1 that are contained in t
    	
    	Lk+1 = get candidates from Ck+1 which satisfy min_support
    ```

6. 문제점
    - DB scan하는 횟수가 너무 많음 (maximum Frequent pattern의 길이만큼 scan해야 함)
    - candidate의 수가 너무 많음
    - Candidate의 support 수를 구하는 계산이 tedious함.
7. 해결책
    - DB scan하는 횟수를 줄이기
    - candidate 수 줄이기
    - candidate의  support counting 용이하게 하기.

## Apriori Improvement

- DB scan 수 횟수 줄이기
- candidate 수 줄이기
- candidate의 support counting 용이하게 하기

### Partition : DB 스캔 수 2회

- 원리
    - whole db를 k개의 local db로 나누어 각 파티션마다 local frequent patterns를 찾음( local min support = min support / k)
- 성질
    - frequent pattern은 k개의 partition 중에 적어도 하나에서 frequent하다는 성질을 이용함.
    - 각 파티션은 메인 메모리에 저장시켜놔야 하므로 k 개를 잘 정하기
- 2번의 Scan
    - 첫 번째 : local partition에서 local frequent pattern을 찾음
    - 두 번째 : whole db를 확인하여 local frequent pattern이 frequent pattern인지 확인하기

### DHC : candidate의 수를 줄임

- 원리
    - candidate-k-itemset이 frequent한지 안한지 조사를 하는 과정에서 k+1-itemset를 위한 hash table을 만듬
    - 먼저 candidate-1-itemset들의 support를 조사하는 와중에 2-itemset들을 조사하여 hash table에 count 수를 증가시켜 저장함.
- candidate-2-itemset을 만들 때 hash table에 저장되어 있는 count 수를 확인하여 min support를 만족하는 itemset들만 candidate를 만듦
    - apriori에서는 candidate를 무조건 만들고 나서 min support를 만족하는지 조사하기에 candidate수가 많을 수 밖에 없다.
    - 하지만 이 방법은 candidate 수를 줄여준다.

### Sampling : DB 스캔하는 수를 줄여줌

- 원리
    - 전체 디비에서 Sample들만 뽑음. 이 샘플 내에서 Apriori를 이용하여 frequent pattern을 찾음.
    - 이 때 Min support는 기존 min support 보다 sample 크기 비율만큼 한 것으로 줄여줘야 함.
- 문제
    - Sample 로부터 찾은 frequent pattern이 전체 디비에서는 frequent 하지 않을 수도 있음
    - Sample에서 찾지 못한 frequent pattern이 전체 디비에 존재할 수 있음
- 해결법 : 스캔을 두 번 더 함
    - 첫 번째 : S와 NB를 조사함. NB(negative border)은 S에는 속해 있지 않지만, subset들은 S에 속하는 itemset들을 말한다. S와 NB가 정말로 frequent한지 infrequent한지를 조사함
    - 두 번째 : 전체 디비를 한 번 더 훑어봐서 missed frequent pattern을 다시 찾아준다. (because of success of nb)

### DIC(Dynamic itemset counting) : DB 스캔 수 줄여줌

- 원리
    - 한 번 subset들의 min support가 조사되어 frequent하다는게 밝혀지는 순간 자기자신이 frequent한지를 찾음

### 여전한 문제점들

- apriori라는 frequent pattern mining method는 candidate-generation-and-test method이기에 너무 많은 DB 스캔 수와 candidate 수를 요구함.
    - frequent pattern의 가장 긴 길이가 k일 경우 db 스캔 수는 이에 비례하며
    - candidate 수의 경우 k^1 + k^2 + k^3 ... 이기 때문에 너무 많음.
- 이를 해결하기 위한 방법으로 FP tree가 등장

## FP-Growh : Mining FP without candidate generation

- 원리 : abc라는 frequent data를 보유하고 있는 transaction들에 "e"가 frequent할 때 abcd도 frequent하다는 것이다.
- FP tree 만들기
    - DB를 한번 스캔해서 f-list를 만들어 줌. (descending order)
    - DB에 들어있는 transaction들을 f-list에 맞추어 정렬함. (ordered frequent items)
    - ordered frequent items들을 가지고 header table과 fp tree 생성
- conditional FP tree 생성하기
    - 이미 생성된 fp tree를 이용하여 frequent pattern들을 구할 수 있다.
    - header table에 들어있는 frequent item을 시작하여 fp tree를 순회한다. frequent pattern p가 가리키는 link를 타고 들어가서 fp tree를 순회하기 시작하는 것이다.
    - 순회할 때마다 p의 transformed prefix path들을 conditional pattern base에 다 저장한다.
        - conditional pattern base : (m - fca : 2, fcab : 1)
    - conditional pattern base마다 이에 해당하는 conditional FP tree를 생성한다.
        - 해당 pattern base의 frequent item에 대한 fp tree를 생성
        - {} ← f : 3 ← c : 3 ← a : 3 ← m
        - m, am, cm, fm, cam, fam, fam, fcam
- conditional fp-tree를 mining 하는 법
    - reculsive하게 연관된 conditional pattern base 들의 FP 트리를 이용하여 mininggka
- Frequent pattern growth
    - 새로운 frequent item들을 recurslively하게 추가하면서 frequent pattern들을 키워나감.
    - 각 frequent item마다 이에 대한 conditinal pattern base 를 만들고 이에 대한 conditional fp tree를 생성함
    - 이 과정을 더 이상 fp tree가 만들어지지 않거나, single path만 생성해 낼까지만 한다.
        - single path는 sup path의 콤비네이션으로 쉽게 구할 수 잇고, 각 콤비네이션은 frequent pattern이다
- 장점
    - Completeness
        - long pattern도 빠짐없이 구할 수 있음
        - lossless complete information을 보존함
    - Compactness
        - irrelevant info들을 제거 가능함 (frequent 한것들만 있기 때문에)
        - DB보다 크기가 작음
        - 자주 발생하는 item들을 더 잘 공유할 수 있도록 descending order을 해놧음
- Divide and conquer
    - 얻어진 frequent pattern을 가지고 mining task와 db를 decompose함
    - smaller database를 가질 수 있음
- others
    - no candidate generation + no candidate test
    - compressed db : fp -tree structure
    - no repeated scan → only twice

## Frequent Pattern들 쉽게 표현하기

max pattern ,closed pattern 사용하면 됨

### Max Miner : max pattern mining

- 원리 : Apriori에 기반
    - frequent 한 1-itemset들을 ascending order로 저장
    - 각 item에 대한 2-itemset들과 potential max pattern을 구함 (set-enumeration tree 사용)
- max pattern을 구하면 그 다음에 candidate 수들을 줄일 수 있음
    - abcd가 max pattern이면 그에 대한 subset들을 구하지 않아도 됨
    - ab가 infrequent하면 abc는 scan할 필요 없음

### CLOSET : closed pattern mining

- 원리 : FP-tree에 의함
    - FP-Growth를 이용하여 같은 support를 가지는 frequent supetset이 존재하지 않는 closed set들을 구함

### CHARM : vertical data format

- 원리
    - 전체 디비를 한 번 스캔하여 vertical data format 형태로 데이터 생성하기
    - k =1 에서부터 시작하여 apriori와 intersection 방법을 이용하여 frequent k itemset으로부터 candidate-k+1 itemset을 구함
- 특징
    - candidate- k-itemset들의 support 수를 찾기 위해서 모든 디비를 다 볼 필요가 없다.
    - item list에 들어있는 tid개수가 결국 support 수이므로 계산은 매우 쉽다
- 문제
    - 하지만 item list가 매우 길고, intersection을 위한 큰 공간이 필요하다.
- 해결
    - diff set을 사용하는 것임

## Association Rules Mining

### Multi-level Association rule mining

- ancestor's rule에 의해서 ancestor와의 관계를 가지는 descendant rule들은 다 제거될 수 있다.
    - 만약, support 수가 예측가능한 수이고
    - confidence 가 둘이 비슷할 때

### Multi-dimension Association rule mining

- single-dimension association rule
- multi-dimension association rule
    - inter-dimension asso rule (no repeated rules)
    - hybrid-dimension asso rule (repeated rules)
- quantitive attributes의 경우에는 clustering이나 discretization으로 카테고리화가 필요하다.
    - Static discretization by predefined concept hierarchies(data cube method)
    - Dynamic discretization based on data distribution

### 한계를 보완하기 위한 Correlation

모든 association rule들에 대한 관심이 없음. correlation을 통해서 관심있는 애들만 보는 거임

- lift  =  P(AUB) / P(A)P(B)
    - lift > 1 : positively related / lift < 1 : positively related
    - lift = 1 : no relation
- cosine = P(AUB) / root(P(A)P(B))
- all_conf = P(X)/ max_item_sup(X)

## Constraint-based Association Mining

너무 방대한 Association rule들을 좀 더 원하는 정보로 보기 위해서 constraint를 거는 것임

### Constraints

- knowledge  type constraint : classification, clustering, association
- data  constraint : 원하는 데이터들만 SQL로 뽑음
- dimension/level constraint : 보고 싶은 attributes
- interestingness constraint : strong rules

- anti-monotonicity
- monotonicity
- succinctness
- tough → 쉽게
