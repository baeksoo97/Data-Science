
import sys
if len(sys.argv) < 3:
    print("Execute the program with three arguments : "
          , "train file name, test file name, output file name")

answer_file = sys.argv[1]
result_file = sys.argv[2]

f_a = open(answer_file, "r")
f_r = open(result_file, "r")

lines_a = f_a.readlines()
lines_r = f_r.readlines()

len_answer = len(lines_a)
len_result = len(lines_r)

correct = 0
for idx in range(1, len(lines_a)):
    if lines_a[idx] == lines_r[idx]:
        correct += 1
    # else:
    #     print("--" ,idx, "--")
    #     print("answer : ", lines_a[idx])
    #     print("result : ", lines_r[idx])

f_a.close()
f_r.close()

# if len_answer != len_result:
    # print("the length of files are not same", len_answer, len_result)

len_answer = len_answer - 1
print(correct, " / ", len_answer)

accuracy = correct / len_answer * 100
print("accuracy : ", accuracy )