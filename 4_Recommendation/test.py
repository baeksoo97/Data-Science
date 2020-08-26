import sys
import numpy as np

def main(test):
    gt = './data/' + test + '.test'
    result = './data/' + test +'.base_prediction.txt'

    fgt = open(gt, 'rb')
    fr = open(result, 'rb')

    gts = fgt.read()
    gts = gts[:-1]
    gts = gts.decode("utf-8")
    ans = gts.split("\n")

    lines = fr.read()
    lines = lines[:-1]
    lines = lines.decode("utf-8")
    line = lines.split("\n")

    loss = 0
    for idx in range(len(line)):
        answer = ans[idx].split("\t")
        data = line[idx].split("\t")
        real_rate = int(answer[2])
        rate = float(data[2])
        loss += (real_rate - rate) * (real_rate - rate)
    loss = np.sqrt(loss/len(line))
    print(loss)

if __name__ == '__main__':
    test = sys.argv[1]

    main(test)
