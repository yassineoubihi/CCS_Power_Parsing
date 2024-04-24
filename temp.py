os.makedirs(output_directory, exist_ok=True)
    directory = 'inputs/'
    files = os.listdir(directory)
    file_handles = {}
    ok_path = "OK/"
    ko_path = "KO/"
    if not os.path.exists(ok_path):
        os.makedirs(ok_path)
    if not os.path.exists(ko_path):
        os.makedirs(ko_path)
    number_of_files = 0
    while number_of_files < len(files):
        file_name = files[number_of_files]
        with open("inputs/" + file_name, 'r') as input_file:
            for line in input_file:
                number = line.split()[0]

                if number not in file_handles:
                    file_handles[number] = open(os.path.join(output_directory, f"{number}.txt"), 'w')
                file_handles[number].write(line)
        for handle in file_handles.values():
            handle.close()
        file_names = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
        i = 0
        while i < len(file_names):
            file_names[i] = output_directory + file_names[i]
            heder = read_lines(file_names[i])
            heder_code = get_heder_code(heder, 1)
            la_long = get_str(heder, 2)
            description_court = get_str(heder, 3)
            code_formule_gestion = get_heder_code(heder, 6)
            description_long = get_str(heder, 7)
            date_service = get_str(heder, 11)
            version_formule_1 = get_heder_code(heder, 12)
            version_formule_2 = get_heder_code(heder, 13)
            ref_1 = get_heder_code(heder, 31)
            ref_2 = get_heder_code(heder, 22)
            c = 0
            heder_id = i
            while int(heder[c].split('|')[1]) != 15:
                c += 1
            while c < len(heder) and int(heder[c].split('|')[1]) != 16:
                comp = get_data_index(heder[c].split('|'), 2)
                cogestion = get_data_index(heder[c].split('|'), 3)
                cousine = get_data_index(heder[c].split('|'), 4)
                codage = get_data_index(heder[c].split('|'), 5)
                num_order = get_data_index(heder[c].split('|'), 6)
                libmp = get_data_index(heder[c].split('|'), 7)
                pct = get_data_index(heder[c].split('|'), 8)
                c += 1
            shutil.move(directory + file_name, str(ok_path) + str(file_name))
            sql_commands = """
            -- Create the database (if your DBMS supports this syntax)
            CREATE DATABASE IF NOT EXISTS mydata;

            USE mydata;

            -- Create the heder table
            CREATE TABLE IF NOT EXISTS heder (
                heder_id INT AUTO_INCREMENT PRIMARY KEY,
                la_long VARCHAR(255) NOT NULL,
                description_court VARCHAR(255) NOT NULL,
                code_formule_gestion VARCHAR(255) NOT NULL,
                description_long VARCHAR(255) NOT NULL,
                date_service VARCHAR(255) NOT NULL,
                version_formule_1 VARCHAR(255) NOT NULL,
                version_formule_2 VARCHAR(255) NOT NULL,
                ref_1 VARCHAR(255) NOT NULL,
                ref_2 VARCHAR(255) NOT NULL
            );

            -- Insert data into heder
            INSERT INTO heder (
                la_long, description_court, code_formule_gestion, 
                description_long, date_service, version_formule_1, 
                version_formule_2, ref_1, ref_2
            ) VALUES ('{}', '{}', '{}',
                    '{}', '{}', '{}',
                    '{}','{}', '{}');

            -- Create the details table
            CREATE TABLE IF NOT EXISTS details (
                heder_id INTEGER,
                heder_code VARCHAR(255),
                comp VARCHAR(255),
                cogestion VARCHAR(255),
                cousine VARCHAR(255),
                codage VARCHAR(255),
                num_order VARCHAR(255),
                libmp VARCHAR(255),
                pct VARCHAR(255),
                FOREIGN KEY (heder_id) REFERENCES heder(heder_id)
            );

            -- Insert data into details
            INSERT INTO details (
                heder_code,comp, cogestion, cousine, codage, num_order, libmp, pct
            ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
            """.format(la_long, description_court, code_formule_gestion,
                    description_long, date_service, version_formule_1,
                    version_formule_2, ref_1, ref_2, heder_code, comp, cogestion, cousine, codage, num_order, libmp, pct)
            with open("database_setup_" + str(i + 1) + ".sql", "w") as file:
                file.write(sql_commands)
            print("here")
            i += 1
            c = 0
        number_of_files += 1