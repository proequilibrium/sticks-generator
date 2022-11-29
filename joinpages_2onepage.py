from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PageObject
import click

def join_pages_2onepage(input_file_name: Path):
    """ """
    with open(input_file_name, "rb") as input_stream:
        # Read the files that you have opened
        pdf_reader = PdfFileReader(input_stream)

        # Make a list of all pages
        pages = []
        page_num = pdf_reader.numPages
        for pageNum in range(page_num):
            pageObj = pdf_reader.getPage(pageNum)
            pages.append(pageObj)

        # Calculate width and height for final output page
        width = pages[0].mediaBox.getWidth()
        height_one = float(pages[0].mediaBox.getHeight())
        height = pages[0].mediaBox.getHeight() * page_num
        # Create blank page to merge all pages in one page
        merged_page = PageObject.createBlankPage(None, width, height)

        # Loop through all pages and merge / add them to blank page
        height_shift = 0.0
        for page in pages:
            merged_page.mergeScaledTranslatedPage(page, 1, 0, height_shift)
            height_shift = height_shift + height_one

        # Create final file with one page
        writer = PdfFileWriter()
        writer.addPage(merged_page)
        output_file_name = Path(input_file_name)
        output_file_name_str = str(output_file_name.parent) + f"_{int(width)}_{int(height)}_" + output_file_name.stem + "_onepage.pdf" 
        writer.write(output_file_name_str)

@click.command()
@click.option("-p", "--path", "path_to_files", default="./export/square", help="Path to files")
def merge_them(path_to_files):
    """ """
    for file in Path(path_to_files).glob("*.pdf"):
        join_pages_2onepage(str(file))


if __name__ == "__main__":
    merge_them()
