import pandas as pd
import subprocess
import pyautogui
import argparse
import time
import os
from datetime import datetime


if __name__ == "__main__":
    interpreter = r"C:\Users\RosaBavarella\Downloads\diffpdf-2.1.3-win32-static (1)\diffpdf.exe"
    parser = argparse.ArgumentParser()
    parser.add_argument("old_pdf_folder", help="")
    parser.add_argument("new_pdf_folder", help="")
    parser.add_argument("output_pdf_folder", help="")

    args = parser.parse_args()
    pdfs_new = [f.replace(".pdf", "") for f in os.listdir(args.new_pdf_folder) if f.endswith(".pdf")]
    output_pdf_folder = os.path.join(args.output_pdf_folder, datetime.strftime(datetime.today(), format="%Y%m%d%H%M%S"))
    os.mkdir(output_pdf_folder)
    
    for pdf in pdfs_new:
        file_old = os.path.join(args.old_pdf_folder, f"{pdf}.pdf")
        file_new = os.path.join(args.new_pdf_folder, f"{pdf}.pdf")
        file_output = os.path.join(output_pdf_folder, f"{pdf}_diff.pdf")
        
        if not os.path.exists(file_output):
            command = [interpreter, file_old, file_new]
            process = subprocess.Popen(command)
            time.sleep(1.5)
            pyautogui.hotkey("alt", "s")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.hotkey("tab")
            pyautogui.write(file_output)
            pyautogui.hotkey("enter")
            time.sleep(1)
            process.terminate()