import sqlite3
import sys
import os


def read_lines(input_path, num_of_lines):
    i = 0
    heder = []
    try:
        with open(input_path, 'r') as file:
            while i < num_of_lines:
                line = file.readline()
                if line == '':
                    break
                heder.append(line.strip())
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

def get_heder_code(heder, index):
    i = 0
    count = 0
    data = heder[index]
    if check_syntax(data) == 1:
        sys.exit("Syntax Error !")
    fields = data.split('|')
    return int(fields[2])

def get_str(heder, index):
    data = heder[index]
    if check_syntax(data) == 1:
        sys.exit("Syntax Error !")
    fields = data.split('|')
    return fields[2]

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
        heder = read_lines(file_names[i], 27)
        heder_code = get_heder_code(heder, 0)
        print("heder_code = " + str(heder_code))
        la_long = get_str(heder, 1)
        print("la long = " + la_long)
        description_court = get_str(heder, 2)
        print("discription court = " + description_court)
        code_formule_gestion = get_heder_code(heder, 5)
        print("code_formule_gestion = " + str(code_formule_gestion))
        description_long = get_str(heder, 6)
        print("description_long = " + description_long)
        date_service = get_str(heder, 12)
        print("date_service = " + date_service)
        version_formule_1 = get_heder_code(heder, 13)
        version_formule_2 = get_heder_code(heder, 14)
        print("version_formule_1 = " + str(version_formule_1))
        print("version_formule_2 = " + str(version_formule_2))
        ref_1 = get_heder_code(heder, 17)
        ref_2 = get_heder_code(heder, 18)
        print("ref_1 = " + str(ref_1))
        print("ref_2 = " + str(ref_2))
        print("--------------------------------------")
        i += 1

if __name__ == "__main__":
    main()
