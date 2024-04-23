import os

def read_lines(input_path, num_of_lines):
    header = []
    try:
        with open(input_path, 'r') as file:
            for _ in range(num_of_lines):
                line = file.readline()
                if not line:
                    break
                header.append(line.strip())
    except FileNotFoundError:
        print(f"The file at {input_path} could not be found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    return header

def check_syntax(data):
    return data.count('|') == 2

def get_header_info(header, num):
    for item in header:
        if not check_syntax(item):
            print("Syntax Error: expected '|'")
            continue
        parts = item.split('|')
        if int(parts[1]) == num:
            return parts[2]
    return "Null"

def process_files(input_path):
    output_directory = 'output_files/'
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    if not os.access(input_path, os.R_OK):
        raise PermissionError(f"The file {input_path} is not readable.")

    os.makedirs(output_directory, exist_ok=True)
    file_handles = {}

    with open(input_path, 'r') as input_file:
        for line in input_file:
            number = line.split('|')[0]
            if number not in file_handles:
                file_handles[number] = open(os.path.join(output_directory, f"{number}.txt"), 'w')
            file_handles[number].write(line)

    for handle in file_handles.values():
        handle.close()

    file_names = [os.path.join(output_directory, f) for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]

    for file_name in file_names:
        header = read_lines(file_name, 27)
        if header is None:
            continue
        print("Header Info:", get_header_info(header, 1))

def main():
    input_path = input("Enter the file Path: ")
    process_files(input_path)

if __name__ == "__main__":
    main()
