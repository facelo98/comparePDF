from pdf2image import convert_from_path
from PIL import Image
import cv2
from pathlib import Path
import numpy as np
import os
import tkinter as tk
from tkinter import ttk


class DiffPdfHandler:
    def __init__(self, pdf_path_1, pdf_path_2, output_path):
        self.pdf_path_1 = pdf_path_1
        self.pdf_path_2 = pdf_path_2
        self.output_path = output_path
        self.poppler_path = os.path.join(Path().parent.parent.absolute(), "src\poppler")
        self.dpi = 200

    def _pil_to_cv2(self, pil_image):
            return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def _highlight_differences(self, img1, img2, alpha=0.3, highlight_color=(180, 105, 255)):
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        has_diff = cv2.countNonZero(thresh) > 0

        if not has_diff:
            return img1, img2, False

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        output1 = img1.copy()
        output2 = img2.copy()
        overlay1 = output1.copy()
        overlay2 = output2.copy()

        for contour in contours:
            if cv2.contourArea(contour) > 20:
                x, y, w, h = cv2.boundingRect(contour)
                padding = 5
                x, y = max(x - padding, 0), max(y - padding, 0)
                w, h = w + 2 * padding, h + 2 * padding
                cv2.rectangle(overlay1, (x, y), (x + w, y + h), highlight_color, -1)
                cv2.rectangle(overlay2, (x, y), (x + w, y + h), highlight_color, -1)

        cv2.addWeighted(overlay1, alpha, output1, 1 - alpha, 0, output1)
        cv2.addWeighted(overlay2, alpha, output2, 1 - alpha, 0, output2)

        return output1, output2, True

    def _combine_images(self, img1, img2):
        height = max(img1.shape[0], img2.shape[0])
        width = img1.shape[1] + img2.shape[1]
        combined = np.zeros((height, width, 3), dtype=np.uint8)

        combined[:img1.shape[0], :img1.shape[1]] = img1
        combined[:img2.shape[0], img1.shape[1]:] = img2

        return combined

    def compare(self):
        pages_pdf_1 = convert_from_path(self.pdf_path_1, poppler_path=self.poppler_path, dpi=self.dpi)
        pages_pdf_2 = convert_from_path(self.pdf_path_2, poppler_path=self.poppler_path, dpi=self.dpi)

        combined_pages = []

        for (page1, page2) in zip(pages_pdf_1, pages_pdf_2):
            cv2_page1 = self._pil_to_cv2(page1)
            cv2_page2 = self._pil_to_cv2(page2)

            out1, out2, has_diff = self._highlight_differences(cv2_page1, cv2_page2)
            combined = self._combine_images(out1, out2)
            combined_image = Image.fromarray(cv2.cvtColor(combined, cv2.COLOR_BGR2RGB))
            combined_pages.append(combined_image)

        if combined_pages:
            combined_pages[0].save(self.output_path,
                                   save_all=True,
                                   append_images=combined_pages[1:],
                                   resolution=100.0)
