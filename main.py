import sys
import os
import tkinter as tk
from tkinter import messagebox, font as tkfont
import threading
import shutil
import time
from tkinter import filedialog, font as tkfont
import smtplib
from email.message import EmailMessage
import ssl
import smtplib


global input_path
input_path = None

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
        i += 1
    if count == 2:
        return 0
    else:
        return 1

def get_heder_code(heder, num, current_working_file, ko_path):
    i = 0
    while i < len(heder):
        if check_syntax(heder[i]) == 1:
            move_file_to = os.path.join(ko_path, os.path.basename(current_working_file))
            if os.path.isfile(current_working_file):
                shutil.move(current_working_file, move_file_to)
            messagebox.showinfo("Syntax Error !" ,"Syntax Error expected '|' in file : " + current_working_file)
            email_sender = 'youbihi129@gmail.com'
            email_password = "falk seer ivkx eolv"

            email_receiver = 'youbihi741@gmail.com'
            msg_subject = 'Syntax Error !'
            body = "Syntax Error expected '|' in file : " + current_working_file

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['subject'] = msg_subject
            em.set_content(body)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            sys.exit(1)
        line = heder[i].split('|')
        if int(line[1]) == num:
            return line[2].strip()
        i += 1
    return -1

def get_str(heder, num):
    i = 0
    while i < len(heder):
        if check_syntax(heder[i]) == 1:
            print("Syntax Error expected '|'")
        line = heder[i].split('|')
        if int(line[1]) == num:
            return line[2].strip()
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

def get_data_start(file, num):
    i = 0
    line_split = file[i].split('|')
    while int(line_split[1]) != num:
        i += 1
        line_split = file[i].split('|')
    return int(i)

def get_data_index(line, index):
    return line[index].strip()


def select_file(path_label, root):
    global input_path
    input_path = filedialog.askopenfilename()  # Open the file dialog
    if input_path:
        path_label.config(text=f"File selected: {input_path}")
        root.quit()  # Close the GUI after file selection
    else:
        path_label.config(text="No file selected.")

def process_file(input_path):
    # Define 'output_directory' where you intend to use it
    output_directory = 'output_files/'
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    if not os.access(input_path, os.R_OK):
        raise PermissionError(f"The file {input_path} is not readable.")

    os.makedirs(output_directory, exist_ok=True)
    # Further processing here...
    print(f"Processing file: {input_path}")

def recurring_task(interval):
    while True:
        os.makedirs(output_directory, exist_ok=True)
        directory = 'inputs/'
        files = os.listdir(directory)
        if not files:
            messagebox.showinfo("Empty Folder", "Folder is empty")
        else :
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
                current_working_file = "inputs/" + file_name
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
                    heder_code = get_heder_code(heder, 1,current_working_file,ko_path)
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
                    move_file_to = os.path.join(ok_path, os.path.basename(current_working_file))
                    if os.path.isfile(current_working_file):
                        shutil.move(current_working_file, move_file_to)
                    i += 1
                    c = 0
                number_of_files += 1
        time.sleep(interval * 60)

def button_command(count_down):
    text = count_down.get()
    try:
        interval = int(text)
        if interval <= 0:
            messagebox.showerror("Error", "Please enter a positive integer for minutes.")
        else:
            thread = threading.Thread(target=recurring_task, args=(interval,), daemon=True)
            thread.start()
            messagebox.showinfo("Success", f"Task scheduled every {interval} minutes.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")


def main():
    global output_directory
    output_directory = 'output_files/'
    root = tk.Tk()
    root.geometry("800x500")
    root.title("CCS Power Parsing")
    root.configure(bg='#aaccb8')

    count_down = tk.Entry(root, width = 100)
    count_down.pack()

    tk.Button(root, text="Enter time between each search", command=lambda: button_command(count_down)).pack()


    label_font = tkfont.Font(family='Helvetica', size=12, weight='bold')
    button_font = tkfont.Font(family='Helvetica', size=12)

    exit_button = tk.Button(root, text="Exit", command=root.quit, font=button_font)
    exit_button.pack(pady=(10, 20), ipadx=10, ipady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
