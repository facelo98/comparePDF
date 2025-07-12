import pyautogui
import time
from PyPDF2 import PdfWriter
import os
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


def wait_for_file_complete(filepath, stable_secs=1):
    last_size = -1
    same_size_since = None
    not_saved = True
    while not_saved:
        if os.path.exists(filepath):
            current_size = os.path.getsize(filepath)
            if current_size == last_size:
                if same_size_since is None:
                    same_size_since = time.time()
                elif time.time() - same_size_since >= stable_secs:
                    not_saved = False
            else:
                same_size_since = None
                last_size = current_size
        time.sleep(0.5)

if __name__ == "__main__":
    executable = os.path.join(Path().parent.absolute(), "diff_pdf\diffpdf.exe")
    root = tk.Tk()
    root.withdraw()
    old_pdf_folder = filedialog.askdirectory(title="Select old pdf folder")
    new_pdf_folder = filedialog.askdirectory(title="Select new pdf folder")
    output_pdf_folder = filedialog.askdirectory(title="Select compare output pdf folder")

    from pywinauto import Application, Desktop
    pdfs_new = [f.replace(".pdf", "") for f in os.listdir(new_pdf_folder) if f.endswith(".pdf")]
    output_pdf_folder = os.path.join(output_pdf_folder, datetime.strftime(datetime.today(), format="%Y%m%d%H%M%S"))
    os.mkdir(output_pdf_folder)

    for pdf in pdfs_new:
        file_old = os.path.join(old_pdf_folder, f"{pdf}.pdf")
        file_new = os.path.join(new_pdf_folder, f"{pdf}.pdf")
        file_output = os.path.join(output_pdf_folder, f"{pdf}_diff.pdf")

        if not os.path.exists(file_output):
            app = Application(backend="uia").start(f'"{executable}" "{file_old}" "{file_new}"')
            dlg = app.window(title_re="DiffPDF")
            dlg.wait('visible', timeout=20)
            if dlg["Custom21"].exists and not dlg["Custom21"].is_enabled():
                writer = PdfWriter()
                writer.add_blank_page(width=595, height=842)
                with open(file_output, "wb") as f:
                    writer.write(f)
            else:
                dlg["Custom21"].click_input()
                save_as = Desktop(backend="uia").window(title_re=".*DiffPDF.*")
                save_as.wait('exists ready visible', timeout=10)
                save_as["Custom9"].click_input()
                pyautogui.write(file_output)
                edit = save_as["Custom9"].child_window(title="Filename:", control_type="Custom").child_window(control_type="Edit")
                save_as['Custom12'].click_input()
                wait_for_file_complete(filepath=file_output)

            dlg.close()