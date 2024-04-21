import os

input_path = 'Formule_0004544.txt'
output_directory = 'output_files/'

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

print("All lines have been organized into separate files .")
