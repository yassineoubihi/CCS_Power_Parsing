import sqlite3
import sys
import os


def read_lines(input_path):
    i = 0
    heder = []
    try:
        with open(input_path, 'r') as file:
            line = file.readline()
            split_line = line.split('|')
            while int(split_line[1]) != 16:
                if line == '':
                    break
                heder.append(line.strip())
                line = file.readline()
                split_line = line.split('|')
                i += 1
    except FileNotFoundError:
        print(f"The file at {input_path} could not be found.")
    except Exception as e:
        print(f"Error: {e}")
    return heder

def check_syntax(data):
    i = 0
    count = 0
    while i < len(data):
        if data[i] == '|':
            count += 1
        i+= 1
    if count == 2:
        return 0
    else:
        return 1

def get_heder_code(heder, num):
    i = 0
    while i < len(heder):
        if check_syntax(heder[i]) == 1:
            print("Syntax Error expected '|'")
        line = heder[i].split('|')
        if int(line[1]) == num:
            return line[2]
        i += 1
    return -1

def get_str(heder, num):
    i = 0
    while i < len(heder):
        if check_syntax(heder[i]) == 1:
            print("Syntax Error expected '|'")
        line = heder[i].split('|')
        if int(line[1]) == num:
            return line[2]
        i += 1
    return "Null"

def get_first_elem(file_content):
    i = 0
    line_split = file_content[i].split('|')
    while int(line_split[1]) != 15:
        i += 1
    return i

def get_by_index(line, index):
    line_split = line.split('|')
    return (line_split[index])

def main():
    output_directory = 'output_files/'
    input_path = input("Enter the file Path : ")
    i = 0
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    if not os.access(input_path, os.R_OK):
        raise PermissionError(f"The file {input_path} is not readable.")

    os.makedirs(output_directory, exist_ok=True)

    file_handles = {}

    with open(input_path, 'r') as input_file:
        for line in input_file:
            number = line.split()[0]

            if number not in file_handles:
                file_handles[number] = open(os.path.join(output_directory, f"{number}.txt"), 'w')
            file_handles[number].write(line)
    for handle in file_handles.values():
        handle.close()
    file_names = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
    print(file_names)
    while i < len(file_names):
        file_names[i] = output_directory + file_names[i]
        heder = read_lines(file_names[i])
        heder_code = get_heder_code(heder, 1)
        la_long = get_str(heder, 2)
        description_court = get_str(heder, 3)
        code_formule_gestion = get_heder_code(heder, 6)
        description_long = get_str(heder, 7)
        print("i am here")
        date_service = get_str(heder, 11)
        version_formule_1 = get_heder_code(heder, 12)
        version_formule_2 = get_heder_code(heder, 13)
        ref_1 = get_heder_code(heder, 31)
        ref_2 = get_heder_code(heder, 22)
        num_of_element = get_heder_code(heder, 18)
        data_loop = 0
        first_elem = get_first_elem(heder)
        c = 0
        """
        while data_loop < num_of_element:
            comp = get_by_index(file_names[i][first_elem], 2)
            cogestion = get_by_index(file_names[i][first_elem], 3)
            cousine = get_by_index(file_names[i][first_elem], 4)
            codage = get_by_index(file_names[i][first_elem], 5)
            num_order = get_by_index(file_names[i][first_elem], 6)
            libmp = get_by_index(file_names[i][first_elem], 7)
            pct = get_by_index(file_names[i][first_elem], 8)
            print("comp = " + comp)
            print("cogestion = " + cogestion)
            print("cousine = " + cousine)
            print("codage = " + codage)
            print("num_order = " + num_order)
            print("libmp = " + libmp)
            print("pct = " + pct)
            data_loop += 1
            """
        i += 1

if __name__ == "__main__":
    main()
