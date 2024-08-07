"""
Modules provide utils for the main parser
"""
import sys
import os
import io
import psycopg2
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
import customtkinter as ctk
from tkinter import filedialog
from datetime import datetime
from PIL import Image
import ipaddress
import io
import glob


global input_path
input_path = None

def check_db_connection():
    if connect_check != True:
        try:
            conn = psycopg2.connect(host = dbhost, dbname= databasename,user= databasename,password="root",port=5432)
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False
    else:
        return True

def update_db_status(label):
    while True:
        path = 'database_connection_fails'
        if check_db_connection():
            label.configure(text="Database ON", text_color='green')
        else:
            if not os.path.exists(path):
                os.mkdir(path)
            file_txt = 'connection_traces.txt'
            full_path = os.path.join(path, file_txt)
            global connectin_fails_msg
            with open(full_path, 'a') as f:
                connectin_fails_msg ="\nConnection Fails at : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(connectin_fails_msg)
            label.configure(text="Database OFF", text_color='red')
        time.sleep(15)

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
        pass
    except Exception as e:
        pass
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

def get_heder_code(current_working_file, num, start):
    while start < len(current_working_file):
        if int(current_working_file[start].split('|')[1]) == num:
            return current_working_file[start].split('|')[2].strip()
        start += 1
    return -1

def get_str(heder, num, start):
    while start < len(heder):
        line = heder[start].split('|')
        if int(line[1]) == num:
            return line[2].strip()
        start += 1
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
    input_path = filedialog.askopenfilename()
    if input_path:
        path_label.config(text=f"File selected: {input_path}")
        root.quit()
    else:
        path_label.config(text="No file selected.")

def process_file(input_path):
    output_directory = 'output_files/'
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"The file {input_path} does not exist.")
    if not os.access(input_path, os.R_OK):
        raise PermissionError(f"The file {input_path} is not readable.")

    os.makedirs(output_directory, exist_ok=True)

def get_data_codage(header, index):
    if (len(header.split('|')[index].strip()) == 0):
        return 0
    else:
        return header.split('|')[index].strip()

def create_header_table(cursor, conn):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS header (
            id SERIAL PRIMARY KEY,
            la_long VARCHAR(255) NOT NULL,
            description_court VARCHAR(255) NOT NULL,
            code_formule_gestion INT NOT NULL,
            description_long VARCHAR(255) NOT NULL,
            date_service VARCHAR(255) NOT NULL,
            version_formule_1 INT NOT NULL,
            version_formule_2 INT NOT NULL,
            ref_1 INT NOT NULL,
            ref_2 INT NOT NULL
        );
    """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS FORMIMP (
                        id          SERIAL PRIMARY KEY,
                        header_id   INTEGER NOT NULL,
                        D_INS       VARCHAR(255),
                        S_COMMENT   VARCHAR(255),
                        C_ETAT      VARCHAR(1)
                    );
    """)
    cursor.execute("COMMENT ON COLUMN FORMIMP.id IS 'Identifiant trace';")
    cursor.execute("COMMENT ON COLUMN FORMIMP.header_id IS 'Identifiant header';")
    cursor.execute("COMMENT ON COLUMN FORMIMP.D_INS IS 'Date insertion';")
    cursor.execute("COMMENT ON COLUMN FORMIMP.S_COMMENT IS 'Commentaire';")
    cursor.execute("COMMENT ON COLUMN FORMIMP.C_ETAT IS 'Etat de l''échange';")


def create_footer_table(cursor, conn):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS table_data (
            id SERIAL PRIMARY KEY,
            header_id INTEGER NOT NULL,
            heder_code INT NOT NULL,
            comp INT NOT NULL,
            cogestion INT NOT NULL,
            cousine VARCHAR(255),
            codage INT NOT NULL,
            num_order INT NOT NULL,
            libmp VARCHAR(255),
            pct REAL,
            FOREIGN KEY (header_id) REFERENCES header(id)
        );
    """)
    conn.commit()

def check_current_working_file(current_working_file,start,decode):
    if decode == "COMP":
        decode_num = 2
    elif decode == "COGESTION":
        decode_num = 3
    elif decode == "COUSINE":
        decode_num = 4
    while start < len(current_working_file) and int(current_working_file[start].split('|')[1]) != 16:
        if not current_working_file[start].split('|')[decode_num].strip():
            return 1
        start += 1
    return 0

def fill_tables(header_id, heder_code, comp, cogestion, cousine, codage, num_order, libmp, pct, curr, conn):
    i = 0
    while i < len(comp):
        create_footer_table(curr, conn)
        curr.execute("""
        INSERT INTO table_data (
        header_id, heder_code, comp, cogestion, cousine, codage,
        num_order, libmp, pct
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (header_id, heder_code, comp[i], cogestion[i], cousine[i], codage[i], num_order[i], libmp[i], pct[i]))
        i += 1

def get_start(start, current_working_file, num):
    while start < len(current_working_file) - 1 and int(current_working_file[start].split('|')[1]) != num:
        start += 1
    if int(current_working_file[start].split('|')[1]) == num:
        return start
    else :
        return -1

def recurring_task(interval):
    flage = 0
    comp = []
    cogestion = []
    cousine = []
    codage = []
    num_order = []
    libmp = []
    pct = []
    num_of_files = 0
    start = 0
    index = 0
    header_id = 0
    error = 0
    file_move = 0
    
    connect_check = True
    conn = psycopg2.connect(host = dbhost, dbname= databasename,user= databasename,password="root",port=5432)
    curr = conn.cursor()

    while True:
        if directory == 'inputs/':
            new_directory = 'inputs/'
        else:
            new_directory = directory + '/'
        if not os.path.exists(new_directory):
            os.mkdir(new_directory)
        txt_files = os.listdir(new_directory)
        txt_files = [file for file in txt_files if file.endswith('.txt')]
        while num_of_files < len(txt_files):
            curr_file = txt_files[num_of_files]
            curr_file = new_directory + curr_file
            with open(curr_file, 'r') as file:
                current_working_file = file.readlines()
            while (get_start(start, current_working_file, 1) != -1):
                start = get_start(start, current_working_file, 1)
                heder_code = get_heder_code(current_working_file,1, start)
                start += 1
                la_long = get_str(current_working_file, 2, start)
                start += 1
                description_court = get_str(current_working_file, 3, start)
                start += 1
                code_formule_gestion = get_heder_code(current_working_file,6, start)
                start += 1
                description_long = get_str(current_working_file, 7, start)
                start += 1
                date_service = get_str(current_working_file, 11, start)
                start += 1
                version_formule_1 = get_heder_code(current_working_file,12, start)
                start += 1
                version_formule_2 = get_heder_code(current_working_file,13, start)
                start += 1
                ref_1 = get_heder_code(current_working_file,31, start)
                start += 1
                ref_2 = get_heder_code(current_working_file,22, start)
                start += 1
                create_header_table(curr,conn)
                start = get_start(start, current_working_file, 14)
                start += 1
                while int(current_working_file[start].split('|')[1]) == 15:
                    curr.execute("SELECT s_valparam FROM config WHERE s_code = 'Decode'")
                    decode = curr.fetchone()
                    if check_current_working_file(current_working_file, start,decode[0]) == 1:
                        error = 1
                        file_move = 1
                        break
                    comp.append (get_data_index(current_working_file[start].split('|'), 2))
                    cogestion.append(get_data_index(current_working_file[start].split('|'), 3))
                    cousine.append(get_data_index(current_working_file[start].split('|'), 4))
                    codage.append(get_data_codage(current_working_file[start], 5))
                    num_order.append(get_data_index(current_working_file[start].split('|'), 6))
                    libmp.append(get_data_index(current_working_file[start].split('|'), 7))
                    pct.append(get_data_index(current_working_file[start].split('|'), 8))
                    start += 1
                if error != 1 :
                    print("data inserted !!!! ")
                    curr.execute("""
                            INSERT INTO header (
                            la_long, description_court, code_formule_gestion, description_long,
                            date_service, version_formule_1, version_formule_2, ref_1, ref_2
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                            """, (la_long, description_court, code_formule_gestion, description_long, 
                            date_service, version_formule_1, version_formule_2, ref_1, ref_2))
                    header_id = curr.fetchone()[0]
                    formule_name = os.path.basename(curr_file)
                    formule_name = formule_name.replace(".txt", "")
                    comment_str = formule_name + " produit numero " + str(heder_code) + " a été traitée"
                    date = datetime.now()
                    date = date.strftime("%Y-%m-%d %H:%M")
                    curr.execute("""
                                 INSERT INTO FORMIMP(
                                     header_id, D_INS, S_COMMENT, C_ETAT
                                 ) VALUES (%s, %s, %s, %s);
                                 """, (header_id, date, comment_str, "A"))
                    fill_tables(header_id, heder_code, comp, cogestion, cousine, codage, num_order, libmp, pct, curr, conn)
                else :
                    curr.execute("""
                            INSERT INTO header (
                            la_long, description_court, code_formule_gestion, description_long,
                            date_service, version_formule_1, version_formule_2, ref_1, ref_2
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                            """, (la_long, description_court, code_formule_gestion, description_long, 
                            date_service, version_formule_1, version_formule_2, ref_1, ref_2))
                    formule_name = os.path.basename(curr_file)
                    formule_name = formule_name.replace(".txt", "")
                    date = datetime.now()
                    date = date.strftime("%Y-%m-%d %H:%M")
                    comment_str = formule_name + " produit numero " + str(heder_code) + " a été traitée"
                    curr.execute("""
                                 INSERT INTO FORMIMP(
                                     header_id, D_INS, S_COMMENT, C_ETAT
                                 ) VALUES (%s, %s, %s, %s);
                                 """, (header_id, date, comment_str, "F"))
                error = 0
            num_of_files += 1
            comp.clear()
            cogestion.clear()
            cousine.clear()
            codage.clear()
            num_order.clear()
            libmp.clear()
            pct.clear()
            
            if file_move == 1:
                destination_path = os.path.join(ko_path, os.path.basename(curr_file))
                shutil.move(curr_file, destination_path)
            elif file_move != 1:
                destination_path = os.path.join(ok_path, os.path.basename(curr_file))
                shutil.move(curr_file, destination_path)
        conn.commit()
        curr.close()
        conn.close()
        connect_check = False
        time.sleep(interval)

def button_command(count_down):
    text = count_down.get()
    conn = psycopg2.connect(host = dbhost, dbname= databasename,user= databasename,password="root",port=5432)
    curr = conn.cursor()
    curr.execute("SELECT s_valparam FROM config WHERE s_code = 'INTERVAL'")
    result = curr.fetchone()

    if not text:
        if result:
            interval_time = int(result[0])
        else:
            curr.execute("""
                INSERT INTO config (
                id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat, s_usermodif
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (1, "INTERVAL", "Interval between each search", "30", datetime.now(), datetime.now(), "user", "user"))
            interval_time = 30
        count_down.delete(0, "end")
        count_down.insert(0, str(interval_time))
    else:
        try:
            interval_time = int(text)
            if interval_time <= 0:
                messagebox.showerror("Error", "Please enter a positive integer for minutes.")
                return
            else:
                if result:
                    curr.execute("UPDATE config SET s_valparam = %s WHERE s_code = 'INTERVAL';", (str(interval_time),))
                else:
                    curr.execute("""
                    INSERT INTO config (
                    id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat, s_usermodif
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (1, "INTERVAL", "Interval between each search", str(interval_time), datetime.now(), datetime.now(), "user", "user"))
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")
            return

    thread = threading.Thread(target=recurring_task, args=(interval_time,), daemon=True)
    thread.start()
    messagebox.showinfo("Success", f"Task scheduled every {interval_time} sec.")
    conn.commit()
    curr.close()
    conn.close()

def open_folder_dialog_ok():
    global ok_path
    default_path = 'OK/'
    selected_folder = filedialog.askdirectory(title="Select a OK folder", initialdir=default_path)
    if selected_folder:
        ok_path = selected_folder
        conn = psycopg2.connect(host=dbhost, dbname=databasename, user=databasename, password="root", port=5432)
        curr = conn.cursor()
        curr.execute("UPDATE config SET s_valparam = %s WHERE s_code = 'DOSFORMOK';", (selected_folder,))
        conn.commit()
        curr.close()
        conn.close()
        path_label_ok.configure(text=f"Folder selected: {selected_folder}")
def open_folder_dialog_ko():
    global ko_path
    default_path = 'KO/'
    selected_folder = filedialog.askdirectory(title="Select a OK folder", initialdir=default_path)
    if selected_folder:
        ko_path = selected_folder
        conn = psycopg2.connect(host=dbhost, dbname=databasename, user=databasename, password="root", port=5432)
        curr = conn.cursor()
        curr.execute("UPDATE config SET s_valparam = %s WHERE s_code = 'DOSFORMKO';", (selected_folder,))
        conn.commit()
        curr.close()
        conn.close()
        path_label_ko.configure(text=f"Folder selected: {selected_folder}")

def open_folder_dialog_directory():
    global directory
    default_path = 'inputs/'
    selected_folder = filedialog.askdirectory(title="Select an Input Directory folder", initialdir=default_path)
    if selected_folder:
        directory = selected_folder
        conn = psycopg2.connect(host=dbhost, dbname=databasename, user=databasename, password="root", port=5432)
        curr = conn.cursor()
        curr.execute("UPDATE config SET s_valparam = %s WHERE s_code = 'DOSFORM';", (selected_folder,))
        conn.commit()
        curr.close()
        conn.close()
        path_label_directory.configure(text=f"Folder selected: {directory}")

def download_files(dbx):
    for entry in dbx.files_list_folder("").entries:
        local_path = os.path.join("background", entry.name)
        metadata, res = dbx.files_download(f"/{entry.name}")
        with open(local_path, "wb") as f:
            f.write(res.content)

def main():
    global output_directory, ok_path, ko_path, directory, connect_check, dbhost, databasename, dosform, fichform, dosformok, dosformko
    connect_check = False
    if not os.path.exists('background'):
                os.mkdir('background')
    with open('file.conf', 'r') as file:
        line = file.readline()
        for line in file:
            if line.split(" ")[0] == "HOST":
                dbhost = ipaddress.ip_address(line.split(" ")[2].strip())
                break
        while line.split(" ")[0] != "DBNAME":
            line = file.readline()
        databasename = line.split(" ")[2].replace("\n", "")
        conn = psycopg2.connect(host = dbhost, dbname= databasename,user= databasename,password="root",port=5432)
        curr = conn.cursor()
        curr.execute("SELECT s_valparam FROM config WHERE s_code = 'DOSFORM'")
        result = curr.fetchone()
        if result:
            directory = result[0]
        else:
            directory = "C:/inputs"
            curr.execute("""
                    INSERT INTO config (
                    id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat,s_usermodif
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (1, "DOSFORM", "inputs files path", "C:/testform", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user", "user"))
        curr.execute("SELECT s_valparam FROM config WHERE s_code = 'FICHFORM'")
        result = curr.fetchone()
        if result:
            pass
        else:
            curr.execute("""
                    INSERT INTO config (
                    id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat,
                    s_usermodif
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (1, "FICHFORM", "txt file name", "formule.txt", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user", "user"))
        curr.execute("SELECT s_valparam FROM config WHERE s_code = 'DOSFORMOK'")
        result = curr.fetchone()
        if result:
            ok_path = result[0]
        else:
            ok_path = "C:/testform/ok"
            curr.execute("""
                    INSERT INTO config (
                    id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat,
                    s_usermodif
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (1, "DOSFORMOK", "OK files path", "C:/testform/ok", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user", "user"))
        curr.execute("SELECT s_valparam FROM config WHERE s_code = 'DOSFORMKO'")
        result = curr.fetchone()
        if result:
            ko_path = result[0]
        else:
            ko_path = "C:/testform/ko"
            curr.execute("""
                    INSERT INTO config (
                    id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat,
                    s_usermodif
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (1, "DOSFORMKO", "KO files path", "C:/testform/ko", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user", "user"))
        conn.commit()
        curr.close()
        conn.close()
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(ok_path):
        os.makedirs(ok_path)
    if not os.path.exists(ko_path):
        os.makedirs(ko_path)
    app = ctk.CTk()
    app.geometry("800x500")
    app.title("CCS Power Parsing")
    app.configure(bg='#aaccb8')
    app.wm_iconbitmap("background/New_Project-removebg-preview.ico")

    my_image = ctk.CTkImage(dark_image=Image.open('background/CCS-power-image.png'),size=(262,80))
    my_label = ctk.CTkLabel(app, text="",image=my_image)
    my_label.pack(pady=10)

    db_status_frame = ctk.CTkFrame(app)
    db_status_frame.pack(fill="x", pady=10, padx=10)
    db_status_label = ctk.CTkLabel(db_status_frame, text="Checking database connection...")
    db_status_label.pack(pady = 5)

    db_thread = threading.Thread(target=update_db_status, args=(db_status_label,), daemon=True)
    db_thread.start()

    frame_directory_container = ctk.CTkFrame(app)
    frame_directory_container.pack(fill="x", pady=10, padx=10)

    frame_directory = ctk.CTkFrame(frame_directory_container)
    frame_directory.pack(fill="x", padx=5, pady=5, ipady=5, ipadx=5)
    frame_directory.configure()
    global path_label_directory
    path_label_directory = ctk.CTkLabel(frame_directory, text=f"Current path is: {directory}")
    path_label_directory.pack(side="left")
    browse_button_directory = ctk.CTkButton(frame_directory, text="Change Input Directory", command=open_folder_dialog_directory)
    browse_button_directory.pack(side="right", padx=10)

    frame_ok_container = ctk.CTkFrame(app)
    frame_ok_container.pack(fill="x", pady=10, padx=10)

    frame_ok = ctk.CTkFrame(frame_ok_container)
    frame_ok.pack(fill="x", padx=5, pady=5, ipady=5, ipadx=5)
    frame_ok.configure()

    global path_label_ok

    path_label_ok = ctk.CTkLabel(frame_ok, text=f"Current path is: {ok_path}")
    path_label_ok.pack(side="left")

    browse_button_ok = ctk.CTkButton(frame_ok, text="Change Folders for OK path", command=open_folder_dialog_ok)
    browse_button_ok.pack(side="right", padx=10)

    frame_ko_container = ctk.CTkFrame(app)
    frame_ko_container.pack(fill="x", pady=10, padx=10)

    frame_ko = ctk.CTkFrame(frame_ko_container)
    frame_ko.pack(fill="x", padx=5, pady=5, ipady=5, ipadx=5)
    frame_ok.configure()

    global path_label_ko

    path_label_ko = ctk.CTkLabel(frame_ko, text=f"Current path is: {ko_path}")
    path_label_ko.pack(side="left")

    browse_button_ko = ctk.CTkButton(frame_ko, text="Change Folders for KO path", command=open_folder_dialog_ko)
    browse_button_ko.pack(side="right", padx=10)
    count_down_container = ctk.CTkFrame(app)
    count_down_container.pack(fill="x", pady=10, padx=10)

    count_down_frame = ctk.CTkFrame(count_down_container)
    count_down_frame.pack(fill="x", padx=5, pady=5, ipady=5, ipadx=5)
    count_down = ctk.CTkEntry(count_down_frame, width=400)
    count_down.pack(side="left", padx=2)
    button = ctk.CTkButton(count_down_frame, text="Enter time between each search", command=lambda: button_command(count_down))
    button.pack(side="right", padx=2, pady=2, ipady=2, ipadx=2)

    exit_button = ctk.CTkButton(app, text="Exit", command=app.quit)
    exit_button.pack(pady=(10, 20), ipadx=10, ipady=5)
    app.mainloop()

if __name__ == "__main__":
    main()
