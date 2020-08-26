## Concept Description이란?

### Descriptive vs Predictive Mining

- Descriptive mining : description concepts or task-relevant data sets in concise, summarative, informative, discriminative forms
- Predictive mining : based on data analysis, constructs a model for the data, and predicts the trend and properties of unknown data based on the model

### Concept Description

- Comparison : provide description of comparison between two or more collection of data
- Characterization : provide a concise and succinct summarization of a given collection of data

### Data Generalization

- concept description에 완전 맞춤이다.
- data set들로 하여금 multiple levels of abstraction에 일반화하도록 한다.
- from lower conceptual levels to higher ones, a process which abstracts data set of task-relevant data in db

### Attribute-oriented induction approach

- relational db query를 이용하여 일차적으로 task-relevant data 를 얻음
- attribute removal or generalization으로 generalization을 실시함
- 위의 generalization을 한 data들을 합침. their respective counts와 함께
- interactive presentation between users

1. Data Focusing : task-relevant data를 얻음 
2. Attribute removal : attribute 내에 많은 값들이 있지만, generalization operator가 존재하지 않아 그냥 attiribute를 삭제함
3. Attribute generalization : attribute 내에 많은 값들이 있고, generalization operator가 존재하면 이를 이용하여 generalize 함
4. Attribute-threshold control : attribute value 갯수를 threshold에 맞춤
5. Generalized relation threshold control  : tuple 갯수를 generalized relation threshold에 맞춤. threshold가 올라갈 수록, drilling down인거고, threshold가 내려갈 수록 rolling up이다.

1. InitialRel : using DMQL
2. PreGen
3. PrimeGen
4. Presentation

### Presentation

- generalized relation
- cross tabulation
- Quantitive characteristic rules

### Comparision

- task relevant data들을 target class와 반대 class로 나눔
- 각 class들을 같은 high level concept에 일반화하여, 튜플들을 비교함
- Quantitive discriminant rules를 사용함
