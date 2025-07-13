import tkinter as tk
from tkinter import filedialog
import sys
from typing import Optional
import os
from datetime import datetime

timestamp = datetime.strftime(datetime.today(), format="%Y%m%d%H%M%S")


def ask_dir(kind: str):
    return filedialog.askdirectory(title=f"Select {kind} file folder")

def check_existence(obj: any) -> Optional[str]:
    if not obj:
        sys.exit()
    return obj


class TypeSelector:
    def __init__(self):
        self.root = None
        self.file_type = None
        self.process_type = None

    def choose_process_type(self):
        label = tk.Label(self.root, text="Do you need only conversion to PDF or also compares?", font=("Helvetica", 12))
        label.pack(pady=20)

        btn_only_conversion = tk.Button(self.root, text="ONLY CONVERSION", width=20,
                                        command=self.select_only_conversion, bg="#FFA500",
                                        fg="white", font=("Helvetica", 10, "bold"))
        btn_only_conversion.pack(side="left", padx=20, pady=20)

        btn_both = tk.Button(self.root, text="ALSO COMPARES", width=20, command=self.select_both, bg="#008000",
                             fg="white", font=("Helvetica", 10, "bold"))
        btn_both.pack(side="right", padx=20, pady=20)

    def select_only_conversion(self):
        self.process_type = "only_conversion"
        self.root.destroy()

    def select_both(self):
        self.process_type = "full"
        self.root.destroy()

    def ask_only_conversion_to_pdf(self):
        self.root = tk.Tk()
        self.root.title("Process type selection")
        self.root.geometry("600x150")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", sys.exit)

    def choose_file_type(self):
        label = tk.Label(self.root, text="Are you working with PDF or RTF files?", font=("Helvetica", 12))
        label.pack(pady=20)

        btn_pdf = tk.Button(self.root, text="PDF", width=10, command=self.select_pdf, bg="#4caf50",
                            fg="white", font=("Helvetica", 10, "bold"))
        btn_pdf.pack(side="left", padx=100, pady=20)

        btn_word = tk.Button(self.root, text="RTF", width=10, command=self.select_word, bg="#2196f3",
                             fg="white", font=("Helvetica", 10, "bold"))
        btn_word.pack(side="right", padx=100, pady=20)

    def ask_file_type(self):
        self.root = tk.Tk()
        self.root.title("Type of files selection")
        self.root.geometry("600x150")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", sys.exit)

    def select_pdf(self):
        self.file_type = ".pdf"
        self.root.destroy()

    def select_word(self):
        self.file_type = ".rtf"
        self.root.destroy()

    def run(self):
        self.ask_file_type()
        self.choose_file_type()
        self.root.mainloop()
        self.ask_only_conversion_to_pdf()
        self.choose_process_type()
        self.root.mainloop()


class DirectoryHandler:
    def __init__(self, file_type: str, process_type: str):
        self.root = None
        self.file_type = file_type
        self.process_type = process_type
        self.old_pdf_folder = None
        self.new_file_folder = None
        self.compare_pdf_folder = None
        self.new_pdf_folder = None
        self.output_pdf_folder = None
        self.files = []

    def make_output_dir(self):
        if self.process_type == "full":
            self.output_pdf_folder = os.path.join(self.compare_pdf_folder, timestamp)
            os.mkdir(self.output_pdf_folder)

    def prepare_directories(self):
        if self.process_type == "full":
            self.old_pdf_folder = check_existence(ask_dir(kind="old PDF"))
            self.new_file_folder = check_existence(ask_dir(kind="new PDF"))
            self.compare_pdf_folder = check_existence(ask_dir(kind="compare PDF"))
        elif self.process_type == "only_conversion":
            self.new_file_folder = check_existence(ask_dir(kind="RTF"))

        self.new_pdf_folder = f"{self.new_file_folder}/pdf" if self.file_type == ".rtf" else self.new_file_folder

        self.files = check_existence(self.list_files(file_type=self.file_type))

    def list_files(self, file_type: str) -> list:
        return [f.replace(file_type, "") for f in os.listdir(self.new_file_folder) if f.endswith(file_type)]

    def create_dialog_box(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def run(self):
        self.create_dialog_box()
        self.prepare_directories()
        self.make_output_dir()
