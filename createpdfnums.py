#!/home/recoder/.virtualenvs/pdfmagic/bin/python
print('script zacina loaduji knihovny...')
from fpdf import FPDF
import time

GEN_START = 134501
GEN_STOP = 149500
GEN_STEP = 800

starttime = time.time()
print("zaciname")

for gen_part_start in range(GEN_START, GEN_STOP, GEN_STEP):

    pdf = FPDF(orientation="L", unit='mm', format=(40,330))

    pdf.set_font('Helvetica')
    pdf.set_font_size(17)
    pdf.set_text_color(90, 90, 90)

    for code in range(gen_part_start, gen_part_start + GEN_STEP):
        pdf.add_page()
        text_code = f"{code}"
        pdf.text(208,35,text_code)
        pdf.text(268,35,text_code)
        if (code % 100) == 0:
            newtime = time.time()
            print(f"vygenerovano: {code} za {newtime - starttime}")
            starttime = newtime
    pdf.output(f"./luggage/data/luggage_{gen_part_start-1}.pdf","F")