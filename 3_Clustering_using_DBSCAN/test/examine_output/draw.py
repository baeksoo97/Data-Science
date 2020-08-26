import numpy as np
import matplotlib.pyplot as plt
import sys
import os

dir_path = "./examine_output/"

def get_cluster(output_file):
    positions = []

    f = open(dir_path + output_file, "r")
    lines = f.readlines()

    for line in lines:
        params = line.split()
        idx = params[0]
        x = float(params[1])
        y = float(params[2])

        positions.append([x, y])

    return np.array(positions)


def get_clusters(output_file_list):
    clusters = []

    for output_file in output_file_list:
        cluster = get_cluster(output_file)
        clusters.append(cluster)

    return clusters


def draw_clusters(clusters, input_file_name, option):
    colors = ['black', 'orange', 'lime',"red","green", "magenta", "brown", "blue",  "purple", "grey", "cyan"]
    plot_name = input_file_name + "_cluster_" + option + ".png"
    print(plot_name)

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))

    for idx, cluster in enumerate(clusters):
        X = cluster[:, 0]
        Y = cluster[:, 1]

        label_name = str(idx) + " : " + str(len(cluster))
        ax.scatter(X, Y, s=0.1, label=label_name, color=colors[idx])

    leg = ax.legend(bbox_to_anchor=[1, 0.75], title="label", fancybox=True)

    for i, text in enumerate(leg.get_texts()):
        plt.setp(text, color=colors[i])

    ax.set_xlabel(plot_name)

    plt.tight_layout()
    plt.savefig(dir_path + plot_name, format='png', dpi=300)
    plt.show()


def draw(clusters):
    labels = ['Group A', 'Group B', 'Group C']
    means = [(0, 0), (2, 4), (-4, 1)]
    covs = [[[1, 0], [0, 1]],  # cov of A
            [[1, 0], [0, 3]],  # cov of B
            [[3, 0], [0, 1]]]  # cov of C
    '''
    NOTE: 그룹별로 2차원 정규분포로부터 100개의 샘플을 추출
    '''
    data = {'Group A': clusters[0],
            'Group B': clusters[1],
            'Group C': clusters[2]}

    print(data)
    #### 2. matplotlib의 figure 및 axis 설정
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    colors = ['salmon', 'orange', 'steelblue']
    markers = ['o', 'x', '^']
    sizes = [20, 40, 60]
    widths = [0.5, 2, 0.5]

    #### 3. scatter plot 그리기
    for i, label in enumerate(labels):
        X = data[label][:, 0]
        Y = data[label][:, 1]
        ax.scatter(X, Y, marker=markers[i])
        # ax.scatter(X, Y, marker=markers[i], color=colors[i], label=label,
        #            s=sizes[i], edgecolor='k', linewidth=widths[i])

    #### 4. Axis 세부설정
    ax.set_xlabel('1st Principal Component')
    ax.set_ylabel('2nd Principal Component')

    #### 5. 범례 나타내기
    ax.legend(loc='best')

    #### 6. 그래프 저장하고 출력하기
    plt.tight_layout()
    # plt.savefig('ex_scatterplot.png', format='png', dpi=300)
    plt.show()


def compare_clusters(ideal_clusters, answer_clusters):
    print("### ideal")
    for idx, cluster in enumerate(ideal_clusters):
        print(idx, len(cluster))

    print("### answer")
    for idx, cluster in enumerate(answer_clusters):
        print(idx, len(cluster))

def main():
    if len(sys.argv) < 3:
        print("please write parameter")
        return

    input_file_name = sys.argv[1]
    output_file_option = sys.argv[2]

    if output_file_option == '1':
        output_file_option = "ideal"
    else:
        output_file_option = "answer"

    file_list = os.listdir("./examine_output")
    ideal_output_file_list = []
    answer_output_file_list = []

    for file in file_list:
        if file == input_file_name + ".txt":
            continue
        if file.startswith(input_file_name):
            if file.endswith("_ideal.txt"):
                continue
            elif file.endswith("_ideal_2.txt"):
                ideal_output_file_list.append(file)
            elif file.endswith("_2.txt"):
                answer_output_file_list.append(file)

    ideal_output_file_list.sort()
    answer_output_file_list.sort()

    ideal_clusters = get_clusters(ideal_output_file_list)
    answer_clusters = get_clusters(answer_output_file_list)

    compare_clusters(ideal_clusters, answer_clusters)

    if output_file_option == "ideal":
        draw_clusters(ideal_clusters, input_file_name, output_file_option)
    else:
        draw_clusters(answer_clusters, input_file_name, output_file_option)
    # draw(clusters)


if __name__ == "__main__":
    main()