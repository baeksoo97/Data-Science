import numpy as np
import sys

data_path = "./data/"


class MF:
    def __init__(self, ratings, k, learning_rate, reg_param, epochs):
        self.ratings = ratings
        self.num_user, self.num_item = ratings.shape
        self.k = k
        self.lr = learning_rate
        self.reg_param = reg_param
        self.epochs = epochs

        self.m_user = np.random.normal(size=(self.num_user, k))
        self.m_item = np.random.normal(size=(self.num_item, k))

        self.b_user = np.zeros(self.num_user)
        self.b_item = np.zeros(self.num_item)
        self.b = np.mean(ratings[np.where(ratings != 0)])

    def train(self):
        for epoch in range(self.epochs):
            for i in range(self.num_user):
                for j in range(self.num_item):
                    if self.ratings[i][j] > 0:
                        self.update_gradient(i, j, self.ratings[i][j])

            cost = self.get_cost()

            if (epoch + 1) % 10 == 0:
                print("epoch : %d -> cost = %.6f" % (epoch + 1, cost))

    def get_cost(self):
        cost = 0
        xi, yi = self.ratings.nonzero()
        self.pred = self.b + self.b_user[:, np.newaxis] + self.b_item[np.newaxis:, ] + self.m_user.dot(self.m_item.T)

        for x, y in zip(xi, yi):
            cost += pow(self.ratings[x, y] - self.pred[x, y], 2)

        return np.sqrt(cost) / len(xi)

    def update_gradient(self, i, j, rating):
        prediction = self.b + self.b_user[i] + self.b_item[j] + self.m_user[i, :].dot(self.m_item[j, :].T)
        error = rating - prediction

        self.b_user[i] += self.lr * (error - self.reg_param * self.b_user[i])
        self.b_item[j] += self.lr * (error - self.reg_param * self.b_item[j])

        d_m = (error * self.m_item[j, :]) - (self.reg_param * self.m_user[i, :])
        d_i = (error * self.m_user[i, :]) - (self.reg_param * self.m_item[j, :])

        self.m_user[i, :] += self.lr * d_m
        self.m_item[j, :] += self.lr * d_i


def get_num_info(file_name):
    file = "./data/" + file_name
    f = open(file, "r")
    lines = f.read().split("\n")

    user_set = set()
    item_set = set()
    max_user = 0
    max_item = 0

    for line in lines:
        param = line.split("\t")
        if len(param) < 2:
            continue
        try:
            user = int(param[0])
            item = int(param[1])
            user_set.add(user)
            item_set.add(item)
            max_user = max(max_user, user)
            max_item = max(max_item, item)
        except:
            print("error", param)

    f.close()

    num_user = max_user + 1
    num_item = max_item + 1

    print("num_user : ", num_user)
    print("num_item : ", num_item)

    return num_user, num_item


def get_ratings(file_name, num_user, num_item):
    train_file = "./data/" + file_name

    ftrain = open(train_file, "r")

    lines = ftrain.read().split("\n")

    ratings = np.zeros([num_user, num_item])

    for line in lines:
        param = line.split("\t")
        if len(param) < 3:
            continue
        try:
            user = int(param[0])
            item = int(param[1])
            rate = int(param[2])
            ratings[user][item] = rate
        except:
            print("error", param)

    ftrain.close()

    ratings = np.array(ratings)

    return ratings


def print_outputs(test_file, train_file, pred):
    test_file = data_path + test_file
    output_file = data_path + train_file + "_prediction.txt"

    ftest = open(test_file, "r")
    lines = ftest.read().split("\n")

    foutput = open(output_file, "w")

    for line in lines:
        param = line.split("\t")
        if len(param) < 2:
            continue
        try:
            user = int(param[0])
            item = int(param[1])
            rate = pred[user][item]
            output_line = str(user) + "\t" + str(item) + "\t" + str(rate) + "\n"
            foutput.write(output_line)
        except:
            print("error : ", param)

    ftest.close()
    foutput.close()


def main():
    if len(sys.argv) < 3:
        print("Please input like below")
        print("python3 recommendation.py u1.base u1.test")
        return

    train_file = sys.argv[1]
    test_file = sys.argv[2]

    num_user, num_item = 1000, 1700

    ratings = get_ratings(train_file, num_user, num_item)

    mf = MF(ratings, k=3, learning_rate=0.01, reg_param=0.01, epochs=100)
    mf.train()

    print_outputs(test_file, train_file, mf.pred)


if __name__ == "__main__":
    main()