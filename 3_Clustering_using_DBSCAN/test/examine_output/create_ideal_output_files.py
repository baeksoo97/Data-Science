import sys
import os

def investigate_output(output_file):
    f = open(output_file, "r")
    lines = f.readlines()

    output = []
    for line in lines:
        line = line.split()
        output.append(line[0])
    f.close()

    return len(output), output


def get_objects(input_file):
    objects = []

    f = open(input_file, "r")

    lines = f.readlines()
    for l_idx, line in enumerate(lines):
        params = line.split()

        idx = int(params[0])
        x = float(params[1])
        y = float(params[2])

        if idx != l_idx:
            print("there is something wrong")
            return

        object = [idx, x, y]
        objects.append(object)

    f.close()

    return objects


def recreate_output_files(input_file, output_file_list):
    objects = get_objects(input_file)

    for file_name in output_file_list:
        f = open(file_name, "r")
        f2 = open(file_name.split(".")[0] + "_2.txt", "w")
        lines = f.readlines()
        for line in lines:
            params = line.split()
            object_idx = int(params[0])

            x = objects[object_idx][1]
            y = objects[object_idx][2]
            info = str(object_idx) + " " + str(x) + " " + str(y) + "\n"
            f2.write(info)

        f.close()
        f2.close()


def main():
    input_file_name = sys.argv[1]
    input_file = input_file_name + ".txt"

    file_list = os.listdir("..")
    ideal_output_file_list = []

    for file in file_list:
        if file == input_file_name + ".txt":
            continue
        if file.startswith(input_file_name):
            if file.endswith("_ideal.txt"):
                ideal_output_file_list.append(file)


    recreate_output_files(input_file, ideal_output_file_list)


if __name__ == "__main__":
    main()