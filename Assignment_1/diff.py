f_a = open("output_answer.txt", "r")

f_m = open("output.txt", "r")

mine_set = set()
answer_set = set()

lines = f_m.readlines()
for line in lines:
    items = line.split()

    mine = " ".join(items)
    mine_set.add(mine)
f_m.close()

lines = f_a.readlines()
for line in lines:
    items = line.split()
    answer = " ".join(items)
    answer_set.add(answer)
f_a.close()

print(len(mine_set))
print(len(answer_set))
# print(mine_set)
# print(answer_set)

print(mine_set.difference(answer_set))
print(mine_set.issubset(answer_set))

if mine_set == answer_set:
    print("it is correct")