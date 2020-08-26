### Data Quality

- accuracy, consistency, timeless, believability, completeness, interpretability

### Data preprocessing

- data cleaning
- data integration
- data reduction
- data transformation, discretization

### Dirty data

- noisy
- incompleteness(missing)
- intentional
- inconsistent

---

## Data Cleaning

- incomplete data → using classification
- noisy data → clustering

---

## Data Integration

서로 다른 source로부터 data를 integrate할 때 여러 문제가 발생할 수 있다.

- entity identification problem
- schema integration
- data value conflicts

redundant data

- object identification
- drived data

redundant data를 잘 찾아서 해결하면 data mining 속도와 퀄리티를 높일 수 있다.

### Correlation Analysis(nominal)

→ chi-square

### Correlation Analysis(numeric)

→ correlation coefficient

### Covariance

---

## Data Reduction

data의 수를 줄이되 같은 data anlaysis 결과를 보여서는 안되는 Data set에서 reduced된 representation을 보이는 것임

- 데이터 수가 너무 많으면 이를 analysis하는데 정말 많은 시간과 코스트가 걸림 이를 줄일 필요가 있음

    ### Dimensionality Reduction

    중요하지 않은 attribute를 제거하는 것 (irrelevant, noisy)

    - curse of dimensionality를 해결할 수 있음(dimensionality가 높아지면, data는 increasingly gkrp sparse해짐. density, distance같은 경우들이 되게 의미가 없어질 수 있음)
    - irrelevant하거나 noisy한 데이터를 피하거나 줄일 수 있음
    - data mining에 있어서 시간과 코스트를 줄일 수 있음
    - 쉬운 visualization을 보임

        ### DWT(Discrete Wavelet Transformation)

        정말 중요한 coefficient를 가지고 오직 작은 fraction만 저장하여 space를 줄이는 것, 하지만 lossy가 존재하긴 하다 .

        compressed approximation이다. 

        linear processing, mutli-resolution analysis이다. 

        ### PCA(Principal Component Analysis)

        오직 numeric data만 다룰 수 있다.

        데이터 속에서 가장 많은 양의 variation을 다룰 수 있는 부분을 capture하여 projection하는 것이다. 

        가장 많은 데이터 variation을 담을 수 있는 orthogonal 한 벡터를 찾아서(principal component) principal component를 내림차순으로 정렬하여, 가장 약한 애들을 제거하여 데이터 수를 줄임

    ### Numerosity Reduction

    data representation에서 alternative, smaller form을 선택함으로서 데이터 볼륨을 줄이는 것

    ### Parametric method

    ### non-parametric method

    sampling, cluster, histogram

    ### Data Compression

    - string compression -loseless
    - audio/video comrpession - lossy
    - time sequence

---

## Data transformation

주어진 attribute 의 value값들을 새로운 대체된 value값 set으로 매핑 시키는 것을 말한다. 

### Normalization

- 더 작고 specified 한 range로 줄이는 것
- min-max normalization, z-score, decimal scaling

### Discretization

- concept hierarchy climbing
- continuous한 아이들
- data size가 줄어들고, 비슷한 애들이 같이 된다.
- binning
    - equal -width
    - equal -depth
   
