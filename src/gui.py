import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from sort import *

def generate_pdfs(csv_file, output_folder):
    # This is your script logic for generating PDFs from the CSV
    try:
        generate_reports(csv_file, output_folder)
        messagebox.showinfo("Success", "PDF files generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_file_var.set(file_path)

def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_var.set(folder_path)

def run_script():
    csv_file = csv_file_var.get()
    output_folder = output_folder_var.get()
    if csv_file and output_folder:
        generate_pdfs(csv_file, output_folder)
    else:
        messagebox.showwarning("Input Error", "Please select both a CSV file and an output folder.")

# Setting up the GUI
root = tk.Tk()
root.title("CSV to PDF Generator")

tk.Label(root, text="Select CSV File:").grid(row=0, column=0, padx=10, pady=5)
csv_file_var = tk.StringVar()
tk.Entry(root, textvariable=csv_file_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_csv_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=5)
output_folder_var = tk.StringVar()
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse...", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Generate PDFs", command=run_script).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
