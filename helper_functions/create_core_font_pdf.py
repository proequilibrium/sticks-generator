from fpdf import FPDF
from pathlib import Path

pdf_path = Path("./output/change_fonts.pdf")


def change_fonts():
    pdf = FPDF()
    pdf.add_page()
    font_sizes = [8, 10, 12, 14]
    for font_size in font_sizes:
        for font in pdf.core_fonts:
            if any([letter for letter in font if letter.isupper()]):
                # skip this font
                continue
            pdf.set_font(font, size=font_size)
            txt = "Font name: {} - {} pts".format(font, font_size)
            pdf.cell(0, 10, txt=txt, ln=1, align="L")
    pdf_path.parents[0].mkdir(parents=True, exist_ok=True)
    pdf.output(pdf_path)


if __name__ == "__main__":
    change_fonts()
