import os
from src import docx_to_pdf
from src.user_interaction import TypeSelector, DirectoryHandler
from src.diff_pdf_handler import DiffPdfHandler
from tqdm import tqdm


if __name__ == "__main__":
    type_selector = TypeSelector()
    type_selector.run()

    directory_handler = DirectoryHandler(file_type=type_selector.file_type,
                                         process_type=type_selector.process_type)
    directory_handler.run()

    if type_selector.file_type in [".rtf", ".docx"]:
        docx_to_pdf.convert(input_path=directory_handler.new_file_folder,
                            output_path=directory_handler.new_pdf_folder,
                            extension=type_selector.file_type)


    if type_selector.process_type == "full":
        for pdf in tqdm(directory_handler.files, desc="Comparing PDFs"):
            file_old = os.path.join(directory_handler.old_pdf_folder, f"{pdf}.pdf")
            file_new = os.path.join(directory_handler.new_pdf_folder, f"{pdf}.pdf")
            file_output = os.path.join(directory_handler.output_pdf_folder, f"{pdf}_diff.pdf")

            if not os.path.exists(file_output):
                DiffPdfHandler(file_old, file_new, file_output).compare()