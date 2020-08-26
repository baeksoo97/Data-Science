import sys
import collections

db = []             # a database of transactions
total_cnt = int()   # the total number of transactions
min_sup = int()     # the minimum support count threshold


def create_first_candidate(db):
    # create first candidate itemset from db
    C1_sup = collections.defaultdict(int)
    for items in db:
        for item in items:
            item = [item]
            C1_sup[tuple(item)] += 1
    return C1_sup


def generate_candidate(Lk, Lk_sup, k):
    # generate candidate k-itemset from frequent (k-1)-itemset
    Ck = []     # candidate k-itemset
    Ck_sup = collections.defaultdict(int)   # candidate k-itemset with support count
    len_Lk = len(Lk)

    for i in range(len_Lk):
        for j in range(i + 1, len_Lk):
            L_first = Lk[i][:-1]
            L_second = Lk[j][:-1]

            # check joinable if first(k-2) items are in common
            if L_first == L_second:
                # join step : join with lexicographic order
                if Lk[i][-1] < Lk[j][-1]:
                    candidate = Lk[i] + tuple([Lk[j][-1]])
                else:
                    candidate = Lk[j] + tuple([Lk[i][-1]])

                # prune step : remove unfruitful candidate
                if has_infrequent_subset(candidate, Lk_sup, k):
                    del(candidate)
                else:
                    Ck.append(candidate)
                    Ck_sup[candidate] = get_support_count_from_db(candidate)

    return Ck, Ck_sup


def has_infrequent_subset(candidate, Lk_sup, k):
    # candidate should be sorted
    for i in range(k + 1):
        subset = candidate[:i] + candidate[i+1:]
        sup = Lk_sup[subset]
        if sup < min_sup:
            return True
    return False


def get_support_count_from_db(candidate):
    # get support count of candidate from db
    cnt = 0
    candidate = set(candidate)
    for transaction in db:
        if candidate.issubset(transaction):
            cnt += 1
    return cnt


def generate_frequent(Ck_sup):
    # generate frequent k-itemset from candidate k-itemset
    Lk = []
    Lk_sup = collections.defaultdict(int)
    for itemset, sup in Ck_sup.items():
        if sup >= min_sup:
            Lk_sup[itemset] = sup
            Lk.append(itemset)
    return Lk, Lk_sup


def get_nonempty_subsets(itemset):
    # get nonempty subsets of itemset
    length = len(itemset)
    subsets = []
    for i in range(1 << length):
        subset = set(itemset[j] for j in range(i) if (i & (1 << j)))
        if subset != set() and subset != set(itemset):
            subsets.append(subset)

    return subsets


def calculate_support_confidence(frequent_itemset_sup, itemset_a, itemset_b):
    # sort union(itemset_a, itemset_b) and itemset_a
    union_itemset = tuple(sorted(itemset_a.union(itemset_b)))
    itemset1 = tuple(sorted(itemset_a))

    # get support count of union(itemset_a, itemset_b) and itemset_a
    sup_union = frequent_itemset_sup[union_itemset]
    sup_itemset_a = frequent_itemset_sup[itemset1]

    # calculate support and confidence of itemset_a and itemset_b
    sup = round(sup_union / total_cnt * 100, 2)
    conf = round(sup_union / sup_itemset_a * 100, 2)

    return sup, conf


if __name__ == "__main__":
    # apriori.py 5 input.txt output.txt
    if len(sys.argv) < 4:
        print("please input min_sup, input_file, output_file")

    min_sup = float(sys.argv[1])
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    f = open(input_file, 'r')
    lines = f.readlines()
    for line in lines:
        items = line.split()
        items = set(int(item) for item in items)
        db.append(items)
    f.close()

    # get the number of transactions from db
    total_cnt = len(db)

    # convert relative minimum support to absolute minimum support
    min_sup = total_cnt * (min_sup / 100)

    # initialize frequent itemset lists
    frequent_itemset = []   # only for itemset
    frequent_itemset_sup = collections.defaultdict(int)    # for itemset and support

    # get candidate and frequent itemset of size 1
    C1_sup = create_first_candidate(db)
    L1, L1_sup = generate_frequent(C1_sup)

    Lk = L1     # frequent itemset of size k
    Lk_sup = L1_sup     # frequent itemset of size k with support
    k = 1

    # generate candidate and frequent itemset of size k
    while True:
        frequent_itemset.append(Lk)
        frequent_itemset_sup.update(Lk_sup)

        # generate candidate itemset of size k from L(k-1)
        Ck, Ck_sup = generate_candidate(Lk, Lk_sup, k)

        # generate frequent itemset of size k from Ck
        Lk, Lk_sup = generate_frequent(Ck_sup)

        k += 1
        if Lk == [] or Ck == []:
            break

    f = open(output_file, "w")
    for k in range(len(frequent_itemset)):
        # avoid frequent itemset of size 1
        if k == 0:
            continue

        # get support and confidence of subsets in frequent itemset
        for itemset in frequent_itemset[k]:
            # get nonempty subsets of itemset
            subsets = get_nonempty_subsets(itemset)

            for itemset_a in subsets:
                itemset_b = set(itemset) - itemset_a

                # get support and confidence of itemset_a and itemset_b
                sup, conf = calculate_support_confidence(frequent_itemset_sup, itemset_a, itemset_b)

                # convert itemset list to string
                itemset_a_str = ",".join(str(s) for s in sorted(itemset_a))
                itemset_b_str = ",".join(str(s) for s in sorted(itemset_b))

                data = "{" + itemset_a_str + "}\t{" + itemset_b_str + "}"
                data += "\t" + str(sup) + "\t" + str(conf) + "\n"

                # write output file
                f.write(data)
    f.close()



