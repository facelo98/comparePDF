import os
from pathlib import Path
from PyPDF2 import PdfWriter
import pyautogui
import time
executable = os.path.join(Path().parent.parent.absolute(), "source\diffpdf.exe")


def wait_save_complete(filepath, stable_secs=1):
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


class DiffPdfHandler:
    def __init__(self, old_file:str, new_file:str, output_file: str):
        self.old_file = Path(old_file).resolve().__str__()
        self.new_file = Path(new_file).resolve().__str__()
        self.output_file = Path(output_file).resolve().__str__()
        self.compare_window = None

    def save_compare_result(self):
        from pywinauto import Desktop
        save_as = Desktop(backend="uia").window(title_re=".*DiffPDF.*")
        save_as.wait('exists ready visible', timeout=10)
        save_as["Custom9"].click_input()
        pyautogui.write(self.output_file)
        save_as['Custom12'].click_input()
        wait_save_complete(filepath=self.output_file)

    def save_empty_pdf(self):
        writer = PdfWriter()
        writer.add_blank_page(width=595, height=842)
        with open(self.output_file, "wb") as f:
            writer.write(f)

    def save_diff(self):
        # Custom21 is "Save As..." button
        if self.compare_window["Custom21"].exists and not self.compare_window["Custom21"].is_enabled():
            self.save_empty_pdf()
        else:
            self.compare_window["Custom21"].click_input()
            self.save_compare_result()

    def compare_files(self):
        from pywinauto import Application
        app = Application(backend="uia").start(f'"{executable}" "{self.old_file}" "{self.new_file}"')
        self.compare_window = app.window(title_re="DiffPDF")
        self.compare_window.wait('visible', timeout=20)

    def compare(self):
        self.compare_files()
        self.save_diff()
        self.compare_window.close()

