# !/usr/bin/python
# Adding a watermark to a single-page PDF

import PyPDF2

import time
import os

starttime = time.time()
print("zaciname generovat watermarky")

source_files = os.listdir("./luggage/data")

for source_file in source_files:

    print(f"Generuji {source_file} *******")

    input_file = "./luggage/data/" + source_file
    output_file = "./luggage/output/" + source_file
    watermark_file = "luggage_back.pdf"

    with open(input_file, "rb") as filehandle_input:
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)
        
        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)
            # create a pdf writer object for the output file
            pdf_writer_output = PyPDF2.PdfFileWriter()
            
            # get first page of the original PDF
            first_page = pdf.getPage(0)
            # get first page of the watermark PDF
            page_watermark = watermark.getPage(0)
            
            for page in range(0, pdf.getNumPages()):
                # merge the two pages
                page_to_write = pdf.getPage(page)
                page_to_write.mergePage(page_watermark)
                        
                # add page
                pdf_writer_output.addPage(page_to_write)

                if (page % 100) == 0:
                    newtime = time.time()
                    print(f"vygenerovano: {page} za {newtime - starttime}")
                    starttime = newtime
                
                        
            with open(output_file, "wb") as filehandle_output:
                # write the watermarked file to the new file
                pdf_writer_output.write(filehandle_output)
