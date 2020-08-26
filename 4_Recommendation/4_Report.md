# Recommendation

## 1.	Summary of Algorithm

I chose “Matrix Factorization” algorithm to predict the ratings of movies in test data by using the given training data containing movie ratings of users. 

Matrix Factorization algorithm is a class of collaborative filtering algorithms. It works by decomposing the user-item interaction matrix into the product of two lower dimensionality rectangular matrices. 

It needs original rating data matrix(ratings), number of users, number of items, dimension of latent factor(k), user latent factor matrix, and item latent factor matrix. I figured out that the source of training and test data is from “MovieLens 100K Dataset”(https://grouplens.org/datasets/movielens/100k/). According to the data set, the number of users is 1700 and the number of items is 1000 so that I just initialized the number of users and items to 1700 and 1000. Also, I set the latent factor of dimension to 3 which is k. And according to testing, I set epoch to 100 which is the most proper value.

To begin training, set all values of matrices or variables that we need by initializing the matrix factorization class. At every epoch, bias and bias matrices for user and item are updated and then user latent factor matrix and item latent factor matrix are also updated by using gradient descent. Then loss function is calculated. When all epochs are finished, the predicted ratings which are updated every epoch would be the result of predicted ratings. And it would be used to predict the test set. And the result of evaluating test set is written in the output file.
 
## 2.	Detailed description of codes
1.	Class MF

This class has original rating data matrix(‘ratings’ matrix), number of users, number of items, the dimension factor of latent(k), user latent factor matrix(‘m_user’ matrix), and item latent factor matrix(‘m_item’ matrix). Also it has bias matrices for user and item latent factor matrices(‘b_user’, ‘b_item’ matrices), and global bias(‘b’) to do regularization. And, it has two hyperparameters which are learning rate and regularization parameter for optimization. 

Predicted ratings are calculated using formula  . They are the sum of bias, bias matrices for user and item, and the dot product between user latent factor matrix and item latent factor matrix. 

And also, I used loss function for optimization. To minimize the result of loss function, user latent factor matrix and item latent factor matrix should be trained. For this optimization, I used gradient descent algorithm. Applying gradient descent algorithm is simple. Loss is differentiated and multiplied by learning rate, then it updates the value of X and Y matrixes.

2.	train() function

```
def train(self):
    for epoch in range(self.epochs):
        for i in range(self.num_user):
            for j in range(self.num_item):
                if self.ratings[i][j] > 0:
                    self.update_gradient(i, j, self.ratings[i][j])

        cost = self.get_cost()

        if (epoch + 1) % 10 == 0:
            print("epoch : %d -> cost = %.6f" % (epoch + 1, cost))
```

As I mentioned, bias matrices for user and item are updated and then user latent factor matrix and item latent factor matrix are also updated by using gradient descent at every epoch using ‘self.update_gradient’ function. Then loss function is calculated by self.get_cost() function. When all epochs are finished, the predicted ratings which are updated every epoch would be the result of predicted ratings.

3.	update_gradient() function

In this function, bias matrices for user and item are updated and then user latent factor matrix and item latent factor matrix are also updated by using gradient descent.
The predicted ratings are calculated by using formula  . 
Error which is the difference between the predicted ratings and actual ratings is used for updating bias matrices and gradients. And gradients of user latent factor and item latent factor are calculated by doing partial derivative for loss regarding to user and item latent factor matrix.

```
def update_gradient(self, i, j, rating):
    prediction = self.b + self.b_user[i] + self.b_item[j] + self.m_user[i, :].dot(self.m_item[j, :].T)
    error = rating - prediction

    self.b_user[i] += self.lr * (error - self.reg_param * self.b_user[i])
    self.b_item[j] += self.lr * (error - self.reg_param * self.b_item[j])

    d_m = (error * self.m_item[j, :]) - (self.reg_param * self.m_user[i, :])
    d_i = (error * self.m_user[i, :]) - (self.reg_param * self.m_item[j, :])

    self.m_user[i, :] += self.lr * d_m
    self.m_item[j, :] += self.lr * d_i
```

4. get_cost()

I used loss function. It is calculated as the sum of square of the difference between the actual rating and the predicted rating. 

```
def get_cost(self):
    cost = 0
    xi, yi = self.ratings.nonzero()
    self.pred = self.b + self.b_user[:, np.newaxis] + self.b_item[np.newaxis:, ] + self.m_user.dot(self.m_item.T)

    for x, y in zip(xi, yi):
        cost += pow(self.ratings[x, y] - self.pred[x, y], 2)

    return np.sqrt(cost) / len(xi) 
```
