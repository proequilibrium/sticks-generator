#!/home/recoder/.virtualenvs/pdfmagic/bin/python
print("script zacina loaduji knihovny...")
from fpdf import FPDF
from create_ean_line import GEN_START, GEN_STOP
import time

starttime = time.time()
print("zaciname")

pdf = FPDF(orientation="L", unit="mm", format=(40, 75))

for code in range(GEN_START, GEN_STOP + 1):
    pdf.add_page()
    # pdf.set_fill_color(0,0,0)
    pdf.image("../data/bar-" + str(code) + ".png", x=7, y=3, w=60, h=35)
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(42, 33, 5, 5, style="F")
    if (code % 100) == 0:
        newtime = time.time()
        print(f"vygenerovano: {code} za {newtime - starttime}")
        starttime = newtime
pdf.output("codes.pdf", "F")
