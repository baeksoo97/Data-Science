import sys
import math
import itertools
from enum import Enum
import os
from ppbtree import *
from tree_format import format_tree

from operator import itemgetter

CLASS_NAME = ""  # "Class:buys_computer"
CLASS_VALUES_IDX = dict()  # {'no': 0, 'yes': 1}

ATTR_NAME = []  # ['age', 'income', 'student', 'credit_rating']
ATTR_IDX = dict()   # {'age': 0, 'income': 1, 'student': 2, 'credit_rating': 3}
ATTR_VALUES_IDX = dict()    # {'age': {'<=30': 0, '31...40': 1, '>40': 2}, 'income': {'high': 0, 'medium': 1, 'low': 2}, # 'student': {'no': 0, 'yes': 1}, 'credit_rating': {'fair': 0, 'excellent': 1}}


class Method(Enum):
    INFORMATION_GAIN = 0
    GAIN_RATIO = 1
    GINI_INDEX = 2


class Node():
    def __init__(self, name="", children=dict(), branch=[], is_leaf=False):
        self.name = ""
        self.children = dict()
        self.branch = []
        self.is_leaf = False

    def set_root(self, attr_name, attr_values):
        self.name = attr_name
        for idx, attr_value in enumerate(attr_values):
            self.branch.append(attr_value)
            self.children[idx] = Node()

    def set_child(self, outcome, child):
        for idx, branch in enumerate(self.branch):
            if branch == outcome:
                self.children[idx] = child
                break

    def set_leaf(self, class_label):
        self.name = class_label
        self.is_leaf = True



def get_unified_class_in_data(data):
    class_value = ""

    for d in data:
        if class_value != "" and class_value != d[-1]:
            return ""
        class_value = d[-1]

    return class_value


def get_majority_class(data):
    majority_class = ""

    num_tuples_having_class = dict()
    for class_value in CLASS_VALUES_IDX.keys():
        num_tuples_having_class[class_value] = 0

    for tuple in data:
        class_value = tuple[-1]
        num_tuples_having_class[class_value] += 1

    max_num = 0
    for class_value, num in num_tuples_having_class.items():
        if max_num < num:
            max_num = num
            majority_class = class_value

    return majority_class


def calculate_p_log(num_Ci_Dj, num_Dj):
    if num_Ci_Dj == 0 or num_Dj == 0:
        return 0
    pi = num_Ci_Dj / num_Dj
    result = - pi * math.log(pi, 2)

    return result


def get_len_tuple_and_base_entropy(data, attr_name, attr_value=""):
    num_total = 0
    num_each_value = [0] * len(CLASS_VALUES_IDX)

    for d in data:
        class_value = d[-1]
        if attr_name == CLASS_NAME or (attr_name != CLASS_NAME and d[ATTR_IDX[attr_name]] == attr_value):

            num_each_value[CLASS_VALUES_IDX[class_value]] += 1
            num_total += 1

    entropy = 0
    for num in num_each_value:
        entropy += calculate_p_log(num, num_total)

    return num_total, entropy


def information_gain(data, attr_list, method):
    splitting_criterion = ""

    len_total_tuple, total_entropy = get_len_tuple_and_base_entropy(data, CLASS_NAME)

    max_entropy = 0
    entropy_criterion = ""
    max_ratio = 0
    ratio_criterion = ""

    for attr_name, attr_values in attr_list.items():
        entropy = 0
        split_info = 0

        for attr_value in attr_values:
            len_satisfied_tuple, base_entropy = get_len_tuple_and_base_entropy(data, attr_name, attr_value)
            entropy += len_satisfied_tuple / len_total_tuple * base_entropy
            split_info += calculate_p_log(len_satisfied_tuple, len_total_tuple)

        gain_entropy = total_entropy - entropy

        if gain_entropy == 0 or split_info == 0:
            gain_ratio = 0
        else:
            gain_ratio = gain_entropy / split_info

        if max_entropy < gain_entropy:
            max_entropy = gain_entropy
            entropy_criterion = attr_name

        if max_ratio < gain_ratio:
            max_ratio = gain_ratio
            ratio_criterion = attr_name

    if method == Method.INFORMATION_GAIN:
        splitting_criterion = entropy_criterion

    elif method == Method.GAIN_RATIO:
        splitting_criterion = ratio_criterion

    return splitting_criterion


def get_len_tuple_and_base_gini(data, attr_name, attr_value=""):
    num_total = 0
    num_each_value = [0] * len(CLASS_VALUES_IDX)
    for d in data:
        class_value = d[-1]
        if attr_name == CLASS_NAME or (attr_name != CLASS_NAME and d[ATTR_IDX[attr_name]] in attr_value):
            num_each_value[CLASS_VALUES_IDX[class_value]] += 1
            num_total += 1

    gini = 0
    if num_total != 0:
        for num in num_each_value:
            gini += math.pow(num / num_total, 2)
    gini = 1.0 - gini

    return num_total, gini


def get_two_divided_subsets_pairs(attr_values):
    pairs = []

    attr_values = set(attr_values)
    num_total = len(attr_values)
    for i in range(1, int(num_total/2) + 1):
        for subset in itertools.combinations(attr_values, i):
            subset = set(subset)
            pair = [subset, attr_values - subset]
            pairs.append(pair)

    return pairs


def gini_index(data, attr_list):
    splitting_criterion = ""

    len_total_tuple, total_gini = get_len_tuple_and_base_gini(data, CLASS_NAME)

    max_gini = 0
    splitting_subsets_pair = []

    for attr_name, attr_values in attr_list.items():
        pairs = get_two_divided_subsets_pairs(attr_values)
        best_gini = 999999999
        best_subsets_pair = []
        for pair in pairs:
            gini = 0
            for subset in pair:
                len_satisfied_tuple, base_gini = get_len_tuple_and_base_gini(data, attr_name, subset)
                gini += len_satisfied_tuple / len_total_tuple * base_gini

            if best_gini >= gini:
                best_gini = gini
                best_subsets_pair = pair

        if max_gini <= total_gini - best_gini:
            max_gini = total_gini - best_gini
            splitting_subsets_pair = best_subsets_pair
            splitting_criterion = attr_name

    return splitting_criterion, splitting_subsets_pair


def get_splitting_criterion(data, attr_list, method):
    splitting_criterion = ""
    splitting_criterion_outcomes = []

    if method != Method.GINI_INDEX:
        splitting_criterion = information_gain(data, attr_list, method)
        splitting_criterion_outcomes = attr_list[splitting_criterion]
    else:
        splitting_criterion, subsets_pair = gini_index(data, attr_list)
        splitting_criterion_outcomes = subsets_pair

    return splitting_criterion, splitting_criterion_outcomes


def get_data_having_outcome(data, splitting_criterion, outcome, method):
    data_having_outcome = []

    criterion_index = ATTR_IDX[splitting_criterion]
    for tuple in data:
        if method != Method.GINI_INDEX:
            if tuple[criterion_index] == outcome:
                data_having_outcome.append(tuple)
        else:
            if tuple[criterion_index] in outcome:
                data_having_outcome.append(tuple)

    return data_having_outcome


def generate_decision_tree(data, attr_list, method):
    node = Node()

    unified_class = get_unified_class_in_data(data)
    if unified_class != "":
        node.set_leaf(unified_class)
        return node

    if len(attr_list) == 0:
        majority_class = get_majority_class(data)
        node.set_leaf(majority_class)
        return node

    splitting_criterion, splitting_criterion_outcomes= get_splitting_criterion(data, attr_list, method)
    node.set_root(splitting_criterion, splitting_criterion_outcomes)

    if method != Method.GINI_INDEX:
        del attr_list[splitting_criterion]

    for outcome in splitting_criterion_outcomes:
        data_having_outcome = get_data_having_outcome(data, splitting_criterion, outcome, method)

        if len(data_having_outcome) == 0:
            majority_class = get_majority_class(data)
            node.set_leaf(majority_class)
            return node
        else:
            node.set_child(outcome, generate_decision_tree(data_having_outcome, attr_list, method))

    return node


def get_class_label_using_model(attr_idx, data, model, method):
    class_label = ""

    root = model
    while True:
        if root.is_leaf:
            class_label = root.name
            break
        else:
            data_idx = int(attr_idx[root.name])
            outcome = data[data_idx]

            for br_idx, br in enumerate(root.branch):
                if method == Method.GINI_INDEX:
                    if outcome in br:
                        root = root.children[br_idx]
                else:
                    if outcome == br:
                        root = root.children[br_idx]

    return class_label


def test_and_create_output(dt_test, dt_result, model, method):
    test_path = os.path.join("./data/", dt_test)
    test_file = open(test_path, "r")

    result_path = os.path.join("./test/", dt_result)
    result_file = open(result_path, "w")

    lines = test_file.readlines()
    attr_idx = dict()
    for l_idx, line in enumerate(lines):
        tuples = line.split()

        if l_idx == 0:
            for idx, tuple in enumerate(tuples):
                attr_idx[tuple] = idx
            tuples.append(CLASS_NAME)
        else:
            class_label = get_class_label_using_model(attr_idx, tuples, model, method)
            tuples.append(class_label)

        output = "\t".join(tuples)
        result_file.write(output)
        result_file.write("\n")

    test_file.close()
    result_file.close()


def get_tree_info(node, branch=""):
    if node.is_leaf:
        node_info = ("%s"%(branch) + " : '" + node.name + "'", [])
        return node_info
    else:
        node_info = ("%s"%(branch) + " : " + node.name, [])
        for child_name, child_node in node.children.items():
            node_info[1].append(get_tree_info(child_node, node.branch[child_name]))
    return node_info


def print_model(model):
    tree = get_tree_info(model)
    print (format_tree(tree, format_node=itemgetter(0), get_children=itemgetter(1)))


def main():
    if len(sys.argv) < 4:
        print("Execute the program with four arguments \n"
              , "[train_file] [test_file] [result_file] [method]\n"
              , "method options : information_gain, gain_ratio, gini_index\n")
        return

    dt_train = sys.argv[1]
    dt_test = sys.argv[2]
    dt_result = sys.argv[3]

    if len(sys.argv) == 4:
        method = "gini_index"
    else:
        method = sys.argv[4]

    if method == "information_gain":
        method = Method.INFORMATION_GAIN
    elif method == "gain_ratio":
        method = Method.GAIN_RATIO
    elif method == "gini_index":
        method = Method.GINI_INDEX
    else:
        print("Please input one method among information_gain, gain_ratio, gini_index")
        print("Ex : python3 dt_py dt_train.txt dt_text.txt dt_result.txt gini_index")
        return

    data_set = []
    train_path = os.path.join("./data/", dt_train)
    f = open(train_path, "r")
    lines = f.readlines()

    attr_values = dict()  # {"age" : {">30","30..40","<40"}, "student" : ["yes","no"]}
    for l_idx, line in enumerate(lines):
        training_tuples = line.split()
        if l_idx == 0:
            ATTR_NAME = training_tuples[:-1]
            for attr_name in ATTR_NAME:
                attr_values[attr_name] = dict()
            CLASS_NAME = training_tuples[-1]

            for idx, name in enumerate(ATTR_NAME):
                ATTR_IDX[name] = idx

        else:
            for idx, attr_value in enumerate(training_tuples[:-1]):
                attr_name = ATTR_NAME[idx]
                if attr_value not in attr_values[attr_name]:
                    size = len(attr_values[attr_name])
                    attr_values[attr_name][attr_value] = size

            class_value = training_tuples[-1]
            if class_value not in CLASS_VALUES_IDX:
                size = len(CLASS_VALUES_IDX)
                CLASS_VALUES_IDX[class_value] = size

            # store training_tuples
            data_set.append(training_tuples)

    f.close()

    ATTR_VALUES_IDX = attr_values

    attr_list = dict()
    for name, values in attr_values.items():
        attr_list[name] = list(values)

    model = generate_decision_tree(data_set, attr_list, method)

    test_and_create_output(dt_test, dt_result, model, method)

    # print_model(model)


if __name__ == "__main__":
    main()