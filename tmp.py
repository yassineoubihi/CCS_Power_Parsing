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

directory = 'inputs/'

if directory == 'inputs/':
        new_directory = 'inputs/'
else:
        new_directory = directory + '/'

if not os.path.exists(new_directory):
        os.mkdir(new_directory)

txt_files = glob.glob(os.path.join(new_directory, "*.txt"))
file = open(txt_files[0],'r')
content = file.read()
print(len(txt_files))

#"""
#        heder = read_lines(file_names[i])
#        heder_code = get_heder_code(heder, 1,current_working_file,ko_path)
#        la_long = get_str(heder, 2)
#        description_court = get_str(heder, 3)
#        code_formule_gestion = get_heder_code(heder, 6, current_working_file,ko_path)
#        description_long = get_str(heder, 7)
#        date_service = get_str(heder, 11)
#        version_formule_1 = get_heder_code(heder, 12,current_working_file,ko_path)
#        version_formule_2 = get_heder_code(heder, 13,current_working_file,ko_path)
#        ref_1 = get_heder_code(heder, 31,current_working_file,ko_path)
#        ref_2 = get_heder_code(heder, 22,current_working_file,ko_path)
#        c = 0
#        create_header_table(curr,conn)
#        curr.execute("""
#            INSERT INTO header (
#            la_long, description_court, code_formule_gestion, description_long,
#            date_service, version_formule_1, version_formule_2, ref_1, ref_2
#            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
#            """, (la_long, description_court, code_formule_gestion, description_long, 
#            date_service, version_formule_1, version_formule_2, ref_1, ref_2))
#        conn.commit()
#"""